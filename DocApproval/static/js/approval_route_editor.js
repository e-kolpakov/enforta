/*global globals*/
(function ($, globals) {
    "use strict";
    //TODO: add real logging/notifying
    var logger = console ? console.log : alert;
    var ui_notifier = logger;

    var wrapper_element = "table";
    var row_element = "tr";
    var cell_element = "td";
    var row_celector = "> tbody > " + row_element;
    var cell_celector = "> tbody > " + row_element + " > " + cell_element;

    var row_button_config = {
        add: {image: "add.png", cssClass: 'btn add_button'},
        remove: {image: "remove.png", cssClass: 'btn remove_button'},
        add_approver: {image: "add.png", cssClass: "btn add_approver_button", caption: "Добавить"}
    };

    function wrap(elem) {
        return "<" + elem + "></" + elem + ">";
    }

    function download_approver_list(target_url) {
        return $.ajax({
            type: 'POST',
            url: target_url,
            dataType: 'json'
        }).promise();
    }

    var Editor = function (target) {
        var that = this;
        var row_count = 0;

        function make_wrapper() {
            return $(wrap(wrapper_element)).addClass("editor-wrapper table table-striped");
        }

        function make_row(row_data) {
            var row = $(wrap(row_element)).attr({'id': "row_" + row_count}).addClass("row");
            make_buttons_cell(row).appendTo(row);
            $(wrap(cell_element)).addClass("step-label").text("Шаг №" + row_count).appendTo(row);
            var steps_cell = $(wrap(cell_element)).addClass("steps").appendTo(row);
            var elements_wrapper = $("<div></div>").attr({'id': "row_wrapper_" + row_count});
            elements_wrapper.addClass("row-fluid").appendTo(steps_cell);
            for (var i = 0; i < row_data.length; i++) {
                make_approver(that.approvers, row_data, row_data[i]).appendTo(elements_wrapper);
            }
            elements_wrapper.append(make_add_approver_button());
            return row;
        }

        function make_approver(approvers, approvers_in_row, selected_approver) {
            var dropdown = make_dropdown(approvers, approvers_in_row, selected_approver);
            return $("<span></span>").addClass("span3").append(dropdown);
        }

        function make_dropdown(approvers, approvers_in_row, selected_approver) {
            var select = $("<select></select>").addClass("input-medium");
            $("<option></option>").text("-----").appendTo(select);
            for (var k in approvers) {
                if (!approvers.hasOwnProperty(k) ||
                    ($.inArray(k, approvers_in_row) != -1 && k != selected_approver))
                    continue;
                var approver = approvers[k];
                var option = $("<option></option>").attr("value", k).text(approver.name);
                select.append(option);
            }
            select.val(selected_approver);
            return select;
        }

        function make_buttons_cell(row) {
            var cell = $(wrap(cell_element)).addClass("span2 buttons-cell");
            make_button(row_button_config.add,function () {
                that.add_row({}, row);
            }).appendTo(cell);
            make_button(row_button_config.remove,function () {
                that.delete_row(row);
            }).appendTo(cell);
            return cell;
        }

        function make_add_approver_button() {
            var span = $("<span></span>").addClass("span3 add-approver");
            make_button(row_button_config.add_approver, function() {
                that.add_approver($(this).parents('span.add-approver'));
            }).appendTo(span);
            return span;
        }

        function make_button(button_cfg, click_handler) {
            var span = $("<span></span>");
            var btn = $("<button></button>").addClass(button_cfg.cssClass).appendTo(span);
            $("<img/>").attr("src", globals.static_root + "img/icons/" + button_cfg.image).appendTo(btn);
            btn.click(click_handler);
            if (button_cfg.caption) {
                span.append(button_cfg.caption);
            }
            return span;
        }

        function relabel_rows() {
            var rows = that.editor_wrapper.find(row_celector);
            for (var i = 0; i < rows.length; i++) {
                var row = rows[i];
                $(row).children(cell_element + ".step-label").text("Шаг №" + (i + 1));
                $(row).attr('id', "row_" + (i + 1));
            }
        }

        function toggle_delete_buttons(enabled) {
            if (enabled)
                that.editor_wrapper.find(cell_celector + "> span > .remove_button").removeAttr('disabled');
            else
                that.editor_wrapper.find(cell_celector + "> span > .remove_button").attr({disabled: 'disabled'});
        }


        this.target = target;
        this.set_data = function (data) {
            that.data = data;
        };
        this.set_approvers = function (approvers) {
            that.approvers = approvers;
        }
        this.render = function () {
            that.editor_wrapper = make_wrapper().appendTo(that.target);
            for (var k in that.data) {
                if (!that.data.hasOwnProperty(k))
                    continue;
                that.add_row(that.data[k]);
            }
        };
        this.add_row = function (data, prev_row) {
            var new_row = make_row(data);
            row_count += 1;
            if (prev_row)
                new_row.insertAfter(prev_row);
            else
                new_row.appendTo(that.editor_wrapper);
            relabel_rows();
            toggle_delete_buttons(row_count != 1);
        };
        this.delete_row = function (row) {
            row.remove();
            row_count -= 1;
            relabel_rows();
            toggle_delete_buttons(row_count != 1);
        };
        this.add_approver = function (marker) {
            make_approver(that.approvers, {}, {}).insertBefore(marker);
        }
    }

    $.fn.approval_route_editor = function (options, initial_data) {
        var target = $(this);
        var csrf = options.csrftoken || $.cookie('csrftoken');
        var $template_list = options.template_list || {};
        if (csrf) {
            $.ajaxSetup({
                beforeSend: function (xhr) {
                    xhr.setRequestHeader("X-CSRFToken", csrf);
                }
            });
        }
        var approver_list_promise = download_approver_list(options.approvers_source_url);
        approver_list_promise.done(function (data, textStatus, jqXHR) {
            logger(data);
            var editor = new Editor(target);
            editor.set_approvers(data);
            editor.set_data(initial_data);
            editor.render();

        });

        // TODO: add real error handling
        approver_list_promise.fail(function (jqXHR, textStatus, errorThrown) {
            ui_notifier(errorThrown);
        });
    };
}(window.jQuery, window.globals));
/*global globals*/
(function ($, globals) {
    "use strict";
    //TODO: add real logging/notifying
    var logger = console ? console.log : alert;
    var ui_notifier = logger;

    var row_button_config = {
        'add': {image: "add.png", cssClass: 'btn add_button'},
        'remove': {image: "remove.png", cssClass: 'btn remove_button'}
    };

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
            return $("<div></div>").addClass("editor-wrapper");
        }

        function make_row(row_data) {
            var row = $("<div></div>").attr({'id': "row_" + row_count}).addClass("row-fluid");
            make_buttons_cell(row).appendTo(row);
            $("<span></span>").addClass("step-label span2").text("Шаг №" + row_count).appendTo(row);
            logger(row_data);
            for (var i=0; i<row_data.length; i++) {
                var dropdown = make_dropdown(that.approvers, row_data, row_data[i]);
                $("<span></span>").addClass("span3").appendTo(row).append(dropdown);
            }
            return row;
        }

        function make_dropdown(approvers, approvers_in_row, selected_approver){
            var select = $("<select></select>").addClass("input-medium");
            $("<option></option>").text("-----").appendTo(select);
            for (var k in approvers){
                if (!approvers.hasOwnProperty(k) ||
                    ($.inArray(k, approvers_in_row) != -1 && k !=selected_approver))
                    continue;
                var approver = approvers[k];
                var option = $("<option></option>").attr("value", k).text(approver.name);
                select.append(option);
            }
            select.val(selected_approver);
            return select;
        }

        function make_buttons_cell(row) {
            var cell = $("<span></span>").addClass("span2 buttons-cell");
            make_button(row_button_config['add'], function(){ that.add_row({},row);}).appendTo(cell);
            make_button(row_button_config['remove'], function(){ that.delete_row(row);}).appendTo(cell);
            return cell;
        }

        function make_button(button_cfg, click_handler){
            var btn = $("<button></button>").addClass(button_cfg.cssClass);
            $("<img/>").attr("src", globals.static_root + "/img/icons/" + button_cfg.image).appendTo(btn);
            btn.click(click_handler);
            return btn;
        }

        function relabel_rows(){
            var rows = that.editor_wrapper.find("> div");
            for (var i=0; i<rows.length; i++){
                var row = rows[i];
                $(row).children("span.step-label").text("Шаг №"+(i+1));
                $(row).attr('id', "row_"+(i+1));
            }
        }

        function toggle_delete_buttons(enabled) {
            if (enabled)
                that.editor_wrapper.find("> div > span > .remove_button").removeAttr('disabled');
            else
                that.editor_wrapper.find("> div > span > .remove_button").attr({disabled: 'disabled'});
        }


        this.target = target;
        this.set_data = function (data) {
            that.data = data;
        };
        this.set_approvers = function(approvers){
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
        this.add_row = function(data, prev_row) {
            var new_row = make_row(data);
            row_count += 1;
            if (prev_row)
                new_row.insertAfter(prev_row);
            else
                new_row.appendTo(that.editor_wrapper);
            relabel_rows();
            toggle_delete_buttons(row_count != 1);
        };
        this.delete_row = function(row) {
            row.remove();
            row_count -= 1;
            relabel_rows();
            toggle_delete_buttons(row_count != 1);
        };
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
/*global globals*/
(function ($, globals) {
    "use strict";

    var Messages = {
        save_success: "Маршрут сохранен",
        save_error: "Произошли ошибки сохранения:\n"
    };

    // TODO: add real logging/notifying
    var logger = function (msg) {
        if (console && console.log) {
            console.log(msg);
        }
    };
    var ui_notifier = alert;

    var Communicator = function (csrf, approver_list_url, approval_route_backend_url) {
        var that = this;
        this.approver_list_url = approver_list_url;
        this.approval_route_backend_url = approval_route_backend_url;

        if (csrf) {
            $.ajaxSetup({
                beforeSend: function (xhr) {
                    xhr.setRequestHeader("X-CSRFToken", csrf);
                }
            });
        }

        this.download_approver_list = function () {
            var ajax_call = $.ajax({
                type: 'POST',
                url: that.approver_list_url,
                dataType: 'json'
            });
            return ajax_call.promise();
        };

        this.save_approval_route = function (approval_route_data) {
            var ajax_call = $.ajax({
                type: 'POST',
                url: that.approval_route_backend_url,
                data: approval_route_data,
                dataType: 'json'
            });
            return ajax_call.promise();
        };
    };

    var HeaderEditor = function (form, controls) {
        function get_element(selector) {
            return $(selector, form);
        }

        var error_class = 'error';

        var pk_input = get_element(controls.pk_input_selector || "#route-pk");
        var name_input = get_element(controls.name_input_selector || "#route-name");
        var desc_input = get_element(controls.desc_input_selector || "#route-description");
        var is_template_input = get_element(controls.is_template_input_selector || "#route-is-template");

        var that = this;
        this.set_data = function (data) {
            pk_input.val(data.pk || 0);
            name_input.val(data.name || '');
            desc_input.val(data.description || '');
            is_template_input.val(data.is_template || false);
        };

        this.validate = function () {
            name_input.parent().removeClass(error_class);
            var result = true;
            if (name_input.val().length === 0) {
                result = false;
                name_input.parent().addClass(error_class);
            }
            return result;
        };

        this.get_data = function () {
            return {
                pk: pk_input.val(),
                name: name_input.val(),
                desc: desc_input.val(),
                is_template: is_template_input.val()
            };
        };
    };

    var Editor = function (target) {
        var that = this;
        var row_count = 0;

        var wrapper_element = "table";
        var row_element = "tr";
        var cell_element = "td";
        var row_celector = "> tbody > " + row_element;
        var cell_celector = "> tbody > " + row_element + " > " + cell_element;
        var approver_selector = cell_element + ".steps span.span-approver > select";

        var row_button_config = {
            add: {image: "add.png", cssClass: 'btn add-button'},
            remove: {image: "remove.png", cssClass: 'btn remove-button'},
            add_approver: {image: "add.png", cssClass: "btn add-approver-button", caption: "Добавить"},
            remove_approver: {image: "close.png", cssClass: "remove-approver-button"}
        };

        function wrap(elem) {
            return "<" + elem + "></" + elem + ">";
        }

        function make_wrapper() {
            return $(wrap(wrapper_element)).addClass("editor-wrapper table table-striped");
        }

        function make_row(row_data) {
            var row = $(wrap(row_element)).attr({'id': "row_" + row_count}).addClass("row");

            make_buttons_cell(row).appendTo(row);
            $(wrap(cell_element)).addClass("step-label").text("Шаг №" + row_count).appendTo(row);

            var steps_cell = $(wrap(cell_element)).addClass("steps").appendTo(row);
            var elements_wrapper = $(wrap("div")).attr({'id': "row_wrapper_" + row_count});
            elements_wrapper.addClass("row-fluid").appendTo(steps_cell);

            for (var i = 0; i < row_data.length; i++) {
                make_approver(that.approvers, row_data[i]).appendTo(elements_wrapper);
            }
            if (!row_data || row_data.length == 0) {
                make_approver(that.approvers).appendTo(elements_wrapper);
            }

            elements_wrapper.append(make_add_approver_button());
            return row;
        }

        function make_approver(approvers, selected_approver) {
            var span = $(wrap("span")).addClass("span3 span-approver");
            make_dropdown(approvers, selected_approver).appendTo(span);

            var remove = $(wrap("span")).addClass("approver-remove").appendTo(span);
            var remove_btn = make_image(row_button_config.remove_approver.image).appendTo(remove);
            remove_btn.addClass(row_button_config.remove_approver.cssClass);
            remove.click(function () {
                that.remove_approver($(this).parents('.span-approver'));
            });

            return span;
        }

        function make_dropdown(approvers, selected_approver) {
            var select = $("<select></select>").addClass("input-medium");
            $("<option></option>").text("-----").attr("value", -1).appendTo(select);
            for (var k in approvers) {
                if (!approvers.hasOwnProperty(k))
                    continue;
                var approver = approvers[k];
                var option = $("<option></option>").attr("value", k).text(approver.name);
                select.append(option);
            }
            if (selected_approver)
                select.val(selected_approver);
            else
                select.val(-1);
            return select;
        }

        function make_buttons_cell(row) {
            var cell = $(wrap(cell_element)).addClass("span2 buttons-cell");
            make_button(row_button_config.add,function () {
                that.add_row([], row);
            }).appendTo(cell);
            make_button(row_button_config.remove,function () {
                that.delete_row(row);
            }).appendTo(cell);
            return cell;
        }

        function make_add_approver_button() {
            var span = $("<span></span>").addClass("span3 add-approver");
            make_button(row_button_config.add_approver,function () {
                that.add_approver($(this).parents('span.add-approver'));
            }).appendTo(span);
            return span;
        }

        function make_button(button_cfg, click_handler) {
            var span = $("<span></span>");
            var btn = $("<button></button>").addClass(button_cfg.cssClass).appendTo(span);
            make_image(button_cfg.image).appendTo(btn);
            btn.click(click_handler);
            if (button_cfg.caption) {
                span.append(button_cfg.caption);
            }
            return span;
        }

        function make_image(src) {
            return $(wrap("img")).attr("src", globals.static_root + "img/icons/" + src);
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
                that.editor_wrapper.find(cell_celector + "> span > .remove-button").removeAttr('disabled');
            else
                that.editor_wrapper.find(cell_celector + "> span > .remove-button").attr({disabled: 'disabled'});
        }

        function get_approvers(row, unique) {
            var approvers_in_step = $(row).find(approver_selector);
            var all_approvers = $.map(approvers_in_step, function (elem) {
                return $(elem).val()
            });
            return (unique) ? $.unique(all_approvers) : all_approvers;
        }


        this.target = target;
        this.set_data = function (data) {
            that.data = data;
        };
        this.set_approvers = function (approvers) {
            that.approvers = approvers;
        }
        this.render = function () {
            var has_rows = false;
            that.editor_wrapper = make_wrapper().appendTo(that.target);
            for (var k in that.data) {
                if (!that.data.hasOwnProperty(k))
                    continue;
                has_rows = true;
                that.add_row(that.data[k]);
            }
            if (!has_rows) {
                that.add_row([]);
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
        this.remove_approver = function (marker) {
            $(marker).remove();
        }

        this.validate = function () {
            var valid = true;
            logger("Validating");
            that.editor_wrapper.find(row_celector).each(function (idx, elem) {
                logger("Validating row " + idx);
                var row_valid = true;
                var all_approvers = get_approvers(elem, false);
                var unique_approvers = get_approvers(elem, true);
                row_valid &= all_approvers.length > 0;
                row_valid &= all_approvers.length == unique_approvers.length;
                row_valid &= all_approvers.indexOf("-1") == -1;

                var row_class = row_valid ? "success" : "error";
                $(elem).removeClass("success error");
                $(elem).addClass(row_class);

                valid &= row_valid;
            });
            return valid;
        }

        this.get_data = function () {
            var result = {};
            that.editor_wrapper.find(row_celector).each(function (idx, elem) {
                logger("Row " + idx + " with id " + $(elem).attr('id'));
                result[idx + 1] = get_approvers(elem, true);
            });
            return result;
        }
    }

    $.fn.approval_route_editor = function (options, initial_data) {
        var target = $(this);
        var csrf = options.csrftoken || $.cookie('csrftoken');

        var comm = new Communicator(csrf, options.approvers_source_url, options.approval_route_backend);
        var editor = new Editor(target);
        var header_editor = new HeaderEditor(options.$form, options.controls);

        function validate_editors() {
            // Both editors needs to be validated, thus can't do
            //  header_editor.validate() && editor.validate() because of short-circuit evaluation of &&
            var header_valid = header_editor.validate();
            var editor_valid = editor.validate();
            return header_valid && editor_valid;
        }

        function save_click_handler(event) {
            event.preventDefault();
            if (validate_editors()) {
                var data = $.extend({}, header_editor.get_data(), { steps: editor.get_data() });
                var save_promise = comm.save_approval_route(data);

                save_promise.done(function (response_data, textStatus, jqXHR) {
                    if (response_data.success) {
                        ui_notifier(Messages.save_success);
                    }
                    else {
                        ui_notifier(Messages.save_error + response_data.errors.join("\n"));
                    }
                });

                save_promise.fail(function (jqXHR, textStatus, errorThrown) {
                    ui_notifier(errorThrown);
                });
            }
            return false;
        }

        header_editor.set_data(initial_data.header_data);

        var approver_list_promise = comm.download_approver_list();
        approver_list_promise.done(function (data, textStatus, jqXHR) {
            editor.set_approvers(data);
            editor.set_data(initial_data.steps);
            editor.render();

            (options.$save_trigger).click(save_click_handler);
        });

        // TODO: add real error handling
        approver_list_promise.fail(function (jqXHR, textStatus, errorThrown) {
            ui_notifier(errorThrown);
        });
    };
}(window.jQuery, window.globals));
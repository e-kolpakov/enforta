/*global globals*/
(function ($, globals, Communicator, ui_manager) {
    "use strict";

    var Messages = {
        save_success: "Маршрут сохранен",
        save_error: "Произошли ошибки сохранения:\n",
        no_templates_available: "Шаблонные маршруты не найдены"
    };

    // TODO: add real logging/notifying
    // TODO: use injection instead of copy-pasting
    var logger = function (msg) {
        if (console && console.log) {
            console.log(msg);
        }
    };

    var HtmlHelper = {

        template_manager_button_config: {
            apply: {image: "apply_template.png", cssClass: 'btn add-button'}
        },

        editor_button_config: {
            add: {image: "add.png", cssClass: 'btn add-button'},
            remove: {image: "remove.png", cssClass: 'btn remove-button'},
            add_approver: {image: "add.png", cssClass: "btn add-approver-button", caption: "Добавить"},
            remove_approver: {image: "close.png", cssClass: "remove-approver-button"}
        },

        create_elem: function (elem) {
            return $("<" + elem + "></" + elem + ">");
        },

        make_button: function (button_cfg, click_handler) {
            var span = this.create_elem("span");
            var btn = this.create_elem("button").addClass(button_cfg.cssClass).appendTo(span);
            this.make_image(button_cfg.image).appendTo(btn);
            btn.click(click_handler);
            if (button_cfg.caption) {
                span.append(button_cfg.caption);
            }
            return span;
        },

        make_image: function (src) {
            return this.create_elem("img").attr("src", globals.static_root + "img/icons/" + src);
        }
    };

    var Comm = function (csrf, approver_list_url, template_route_source_url, approval_route_backend_url) {
        var ajax_comm = new Communicator(csrf);

        this.download_approver_list = function () {
            return ajax_comm.make_request({url: approver_list_url});
        };

        this.download_template_list = function () {
            return ajax_comm.make_request({url: template_route_source_url});
        };

        this.save_approval_route = function (approval_route_data) {
            return ajax_comm.make_request({url: approval_route_backend_url, data: approval_route_data});
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

        function set_controls_availability(is_template) {
            var ctrls = name_input.add(desc_input);
            if (!is_template) {
                ctrls.attr('disabled', true);
            } else {
                ctrls.removeAttr('disabled');
            }
        }

        function set_ctrl_data($ctrl, data, safe) {
            if (!safe || $ctrl.val() === '') {
                $ctrl.val(data);
            }
        }

        var that = this;
        this.set_data = function (data, safe_set) {
            var eff_safe = safe_set || false;
            var is_template = data.is_template || false;

            set_ctrl_data(pk_input, data.pk || 0, true);
            set_ctrl_data(is_template_input, data.is_template || 0, true);
            set_ctrl_data(name_input, data.name || '', eff_safe || !is_template);
            set_ctrl_data(desc_input, data.description || '', eff_safe || !is_template);

            if (!eff_safe) {
                set_controls_availability(is_template);
            }
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

    var TemplateManager = function ($placeholder, apply_template_callback) {
        var that = this;
        var templates = {};
        var table;

        function create_table() {
            $placeholder.empty();
            table = HtmlHelper.create_elem("table").addClass("table table-striped").appendTo($placeholder);
        }

        function create_row(template_id, template_data) {
            var row = HtmlHelper.create_elem('tr');
            HtmlHelper.create_elem('td').text(template_data.name).appendTo(row);
            var apply_template_button = HtmlHelper.make_button(
                HtmlHelper.template_manager_button_config.apply,
                function () {
                    apply_template_callback(template_data);
                }
            );
            HtmlHelper.create_elem('td')
                .addClass('apply-template-button-cell')
                .append(apply_template_button)
                .appendTo(row);
            return row;
        }

        function create_no_data_row() {
            var row = HtmlHelper.create_elem('tr');
            HtmlHelper.create_elem('td').text(Messages.no_templates_available).appendTo(row);
            return row;
        }

        this.set_data = function (data) {
            templates = data;
        };

        this.render = function () {
            var has_data = false;
            create_table();
            for (var template_id in templates) {
                if (!templates.hasOwnProperty(template_id)) continue;
                has_data = true;
                create_row(template_id, templates[template_id]).appendTo(table);
            }
            if (!has_data) {
                create_no_data_row().appendTo(table);
                ;
            }
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

        function make_wrapper() {
            return HtmlHelper.create_elem(wrapper_element).addClass("editor-wrapper table table-striped");
        }

        function make_row(row_data) {
            var row = HtmlHelper.create_elem(row_element).attr({'id': "row_" + row_count}).addClass("row");

            make_buttons_cell(row).appendTo(row);
            HtmlHelper.create_elem(cell_element).addClass("step-label").text("Шаг №" + row_count).appendTo(row);

            var steps_cell = HtmlHelper.create_elem(cell_element).addClass("steps").appendTo(row);
            var elements_wrapper = HtmlHelper.create_elem("div").attr({'id': "row_wrapper_" + row_count});
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
            var span = HtmlHelper.create_elem("span").addClass("span3 span-approver");
            make_dropdown(approvers, selected_approver).appendTo(span);

            var remove = HtmlHelper.create_elem("span").addClass("approver-remove").appendTo(span);
            var remove_btn = HtmlHelper.make_image(HtmlHelper.editor_button_config.remove_approver.image).appendTo(remove);
            remove_btn.addClass(HtmlHelper.editor_button_config.remove_approver.cssClass);
            remove.click(function () {
                that.remove_approver($(this).parents('.span-approver'));
            });

            return span;
        }

        function make_dropdown(approvers, selected_approver) {
            var select = HtmlHelper.create_elem("select").addClass("input-medium");
            HtmlHelper.create_elem("option").text("-----").attr("value", -1).appendTo(select);
            for (var k in approvers) {
                if (!approvers.hasOwnProperty(k))
                    continue;
                var approver = approvers[k];
                var option = HtmlHelper.create_elem("option").attr("value", k).text(approver.name);
                select.append(option);
            }
            if (selected_approver)
                select.val(selected_approver);
            else
                select.val(-1);
            return select;
        }

        function make_buttons_cell(row) {
            var cell = HtmlHelper.create_elem(cell_element).addClass("span2 buttons-cell");
            HtmlHelper.make_button(HtmlHelper.editor_button_config.add,function () {
                that.add_row([], row);
            }).appendTo(cell);
            HtmlHelper.make_button(HtmlHelper.editor_button_config.remove,function () {
                that.delete_row(row);
            }).appendTo(cell);
            return cell;
        }

        function make_add_approver_button() {
            var span = HtmlHelper.create_elem("span").addClass("span3 add-approver");
            HtmlHelper.make_button(HtmlHelper.editor_button_config.add_approver,function () {
                that.add_approver($(this).parents('span.add-approver'));
            }).appendTo(span);
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

        function clean() {
            if (that.editor_wrapper)
                that.editor_wrapper.remove();
            row_count = 0;
        }


        this.target = target;
        this.set_data = function (data, no_render) {
            var eff_no_render = no_render || false;
            that.data = data;
            if (!eff_no_render) {
                that.render();
            }
        };
        this.set_approvers = function (approvers) {
            that.approvers = approvers;
        }
        this.render = function () {
            clean();
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
            make_approver(that.approvers, {}).insertBefore(marker);
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
    };

    $.fn.approval_route_editor = function (options, initial_data) {
        var target = $(this);

        var comm = new Comm(options.csrftoken, options.approvers_source_url, options.template_route_source_url, options.approval_route_backend);
        var editor = new Editor(target);
        var header_editor = new HeaderEditor(options.$form, options.controls);
        var template_manager = new TemplateManager(options.$template_routes_pane, apply_template);

        function validate_editors() {
            // Both editors needs to be validated, thus can't do
            //  header_editor.validate() && editor.validate() because of short-circuit evaluation of &&
            var header_valid = header_editor.validate();
            var editor_valid = editor.validate();
            return header_valid && editor_valid;
        }

        function apply_template(template_data) {
            editor.set_data(template_data.steps);
            header_editor.set_data(template_data, true);
        }

        function save_click_handler(event) {
            event.preventDefault();
            if (validate_editors()) {
                var data = $.extend({}, header_editor.get_data(), { steps: editor.get_data() });
                var save_promise = comm.save_approval_route(data);

                save_promise.done(function (response_data, textStatus, jqXHR) {
                    if (response_data.success) {
                        ui_manager.message(Messages.save_success);
                    }
                    else {
                        ui_manager.message(Messages.save_error + response_data.errors.join("\n"));
                    }
                });

                save_promise.fail(function (jqXHR, textStatus, errorThrown) {
                    ui_manager.message(errorThrown);
                });
            }
            return false;
        }

        function revert_click_handler(event) {
            event.preventDefault();
            editor.set_data(initial_data.steps);
            header_editor.set_data(initial_data.header_data);
            return false;
        }

        header_editor.set_data(initial_data.header_data);

        var approver_list_promise = comm.download_approver_list();
        var template_list_promise = comm.download_template_list();

        approver_list_promise.done(function (data, textStatus, jqXHR) {
            editor.set_approvers(data);
            editor.set_data(initial_data.steps);

            (options.$save_trigger).click(save_click_handler);
            (options.$revert_trigger).click(revert_click_handler);
        });

        template_list_promise.done(function (data, textStatus, jqXHR) {
            template_manager.set_data(data);
            template_manager.render();
        });

        // TODO: add real error handling
        approver_list_promise.fail(function (jqXHR, textStatus, errorThrown) {
            ui_manager.message(errorThrown);
        });

        template_list_promise.fail(function (jqXHR, textStatus, errorThrown) {
            ui_manager.message(errorThrown);
        });
    };
}(window.jQuery, window.globals, AjaxCommunicator, UiManager));
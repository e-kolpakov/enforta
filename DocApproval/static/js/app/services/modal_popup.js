/*global define*/
define(
    ['jquery', 'extend', 'bootstrap'],
    function ($, extend) {
        var button_types = {
            ok: {text: 'OK', cssClass: 'btn btn-primary', id: 'btn-ok'},
            save: {text: 'Сохранить', cssClass: 'btn btn-primary', id: 'btn-save'},
            cancel: {text: 'Отменить', cssClass: 'btn btn-secondary', id: 'btn-cancel'},
            approve: {text: 'Утвердить', cssClass: 'btn btn-primary', id: 'btn-approve'},
            reject: {text: 'Отклонить', cssClass: 'btn btn-primary', id: 'btn-reject'}
        };

        function make_elem(elem) {
            return $("<" + elem + "></" + elem + ">");
        }

        function make_button(btn_config, anchor, callback) {
            make_elem("button").addClass(btn_config.cssClass).text(btn_config.text).appendTo(anchor).click(callback);
        }

        function make_bootstrap_form() {
            return make_elem('form').addClass('form-horizontal');
        }

        function make_bootstrap_form_rows(form, controls) {
            for (var i = 0; i < controls.length; i++) {
                var row = make_elem('div').addClass('control-group');
                var control = controls[i];
                if (control.label) {
                    make_elem("label").text(control.label).addClass('control-label')
                        .attr('for', control.id).appendTo(row);
                }
                var ctrls = make_elem("div").addClass("controls").appendTo(row);
                var all_attributes = $.extend({id: control.id}, control.attributes);
                var input_ctrl = make_elem(control.type).attr(all_attributes);
                if (control.cssClass) {
                    input_ctrl.addClass(control.cssClass);
                }
                if (control.initial) {
                    input_ctrl.val(control.initial);
                }
                input_ctrl.appendTo(ctrls);
                row.appendTo(form);
            }
        }

        function ModalPopup() {
            this.fragments = this.create_fragments();
        }

        ModalPopup.prototype = new function () {
            this.create_fragments = function () {
                var result = {};
                result.popup = make_elem("div").addClass("modal hide fade").attr({
                    'role': 'dialog',
                    'aria-labelledby': 'popup-label',
                    'aria-hidden': 'true'
                });
                result.header = make_elem("div").addClass("modal-header").appendTo(result.popup);
                make_elem("button").addClass("close").text('x')
                    .attr({'data-dismiss': 'modal', 'aria-hidden': 'true'})
                    .appendTo(result.header);
                result.caption = make_elem("h4").attr("id", 'popup-label').appendTo(result.header);
                result.body = make_elem("div").addClass("modal-body").appendTo(result.popup);
                result.footer = make_elem("div").addClass("modal-footer").appendTo(result.popup);
                return result;
            };

            this.set_buttons = function (buttons) {
                var eff_buttons = buttons || {};

                for (var btn in eff_buttons) {
                    if (!eff_buttons.hasOwnProperty(btn) || !button_types.hasOwnProperty(btn)) continue;
                    make_button(button_types[btn], this.fragments.footer, buttons[btn]);
                }
            };

            this.set_header = function (header) {
                this.fragments.caption.empty();
                this.fragments.caption.text(header);
            };

            this.set_label = function (message) {
                this.fragments.body.empty();
                this.fragments.body.text(message);
            };

            this.show = function () {
                this.fragments.popup.modal({
                    backdrop: true,
                    keyboard: true
                });
            };

            this.hide = function () {
                this.fragments.popup.modal('hide');
            };

            this.dispose = function () {
                this.hide();
                this.fragments.popup.empty();
                this.fragments.popup.remove();
                delete this.fragments;
            };
        };

        function ApproveActionPopup() {
            this.fragments = this.create_fragments();
        }

        extend(ApproveActionPopup, ModalPopup);
        (function () {
            ApproveActionPopup.prototype.create_controls = function (with_on_behalf, on_behalf_list) {
                var form = make_bootstrap_form();
                var controls = [
                    {
                        type: 'textarea',
                        label: this.comment_label || "Комментарий",
                        id: 'action-reason',
                        attributes: {rows: 10},
                        cssClass: 'input-xlarge'
                    }
                ];
                make_bootstrap_form_rows(form, controls);
                form.appendTo(this.fragments.body);
            };

            ApproveActionPopup.prototype.set_label = function (label) {
                this.comment_label = label;
            };

            ApproveActionPopup.prototype.get_data = function () {
                return {
                    comment: $('#action-reason', this.fragments.body).val()
                };
            };
        }());

        function DateInputModalPopup() {
            this.fragments = this.create_fragments();
        }

        extend(DateInputModalPopup, ModalPopup);
        (function () {
            DateInputModalPopup.prototype.create_controls = function (with_on_behalf, on_behalf_list) {
                var form = make_bootstrap_form();
                var controls = [
                    {
                        type: 'input',
                        label: this.date_paid_label || "Дата оплаты",
                        id: 'paid-date',
                        attributes: {type: 'text'},
                        cssClass: 'datepicker'
                    }
                ];
                make_bootstrap_form_rows(form, controls);
                form.appendTo(this.fragments.body);
                $(".datepicker", this.fragments.body).wrapped_datepicker({
                    showButtonPanel: true
                });
            };

            DateInputModalPopup.prototype.set_label = function (label) {
                this.date_paid_label = label;
            };

            DateInputModalPopup.prototype.get_data = function () {
                return {
                    paid_date: $('#paid-date', this.fragments.body).val()
                };
            };
        }());

        return {
            basic_popup_class: ModalPopup,
            approve_action_popup_class: ApproveActionPopup,
            date_input_modal_popup_class: DateInputModalPopup,
            buttons_config: button_types
        };
    }
)
;
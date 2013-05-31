/*global define*/
define(
    ['jquery', 'bootstrap'],
    function ($) {
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

        function ModalPopup() {
            var that = this;

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

                for (var btn in buttons) {
                    if (!buttons.hasOwnProperty(btn) || !button_types.hasOwnProperty(btn)) continue;
                    make_button(button_types[btn], that.fragments.footer, buttons[btn]);
                }
            };

            this.set_header = function (header) {
                that.fragments.caption.empty();
                that.fragments.caption.text(header);
            };

            this.set_content = function (message) {
                that.fragments.body.empty();
                that.fragments.body.text(message);
            };

            this.show = function () {
                that.fragments.popup.modal({
                    backdrop: true,
                    keyboard: true
                });
            };

            this.hide = function () {
                that.fragments.popup.modal('hide');
            };

            this.dispose = function () {
                that.hide();
                that.fragments.popup.empty();
                that.fragments.popup.remove();
                delete that.fragments;
            };

            this.fragments = this.create_fragments();
        }

        return {
            basic_popup_class: ModalPopup,
            buttons_config: button_types
        };
    }
);
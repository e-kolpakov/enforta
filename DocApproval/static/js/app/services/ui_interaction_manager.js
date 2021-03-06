/*global define*/
define(
    ['jquery', 'app/services/modal_popup'],
    function ($, modal_popup_module_exports) {
        var BasicPopupClass = modal_popup_module_exports.basic_popup_class;
        var ApproveActionPopupClass = modal_popup_module_exports.approve_action_popup_class;
        var DateInputModalPopup = modal_popup_module_exports.date_input_modal_popup_class;
        var modal_buttons_config = modal_popup_module_exports.buttons_config;

        function UIManager() {
            var that = this;

            function instantiate_modal(caption, message, dlg_class) {
                var DialogClass = dlg_class || BasicPopupClass;
                var popup = new DialogClass();
                if (message)
                    popup.set_label(message);
                if (caption)
                    popup.set_header(caption);
                return popup;
            }

            this.message = function (message, caption) {
                var eff_caption = caption || "Сообщение";
                var popup = instantiate_modal(eff_caption, message);
                popup.set_buttons({ok: function () {
                    popup.dispose();
                }});
                popup.show();
            };
            this.error = function (message) {
                that.message(message, "Ошибка");
            };
            this.confirmation = function (question, callback, caption) {
                var eff_caption = caption || "Подтверждение";
                var popup = instantiate_modal(eff_caption, question);
                popup.set_buttons({
                    ok: function () {
                        popup.dispose();
                        callback(true);
                    },
                    cancel: function () {
                        popup.dispose();
                        callback(false);
                    }
                });
                popup.show();
            };
            this.input = function (caption, action, request_pk, callback) {
                var popup = instantiate_modal(caption, "Комментарий", ApproveActionPopupClass);

                function handle(success) {
                    var data = popup.get_data();
                    popup.dispose();
                    callback($.extend({}, data, {success: success}));
                }

                popup.create_controls(action, request_pk);
                popup.set_buttons({
                    ok: function () {
                        handle(true);
                    },
                    cancel: function () {
                        handle(false);
                    }
                });
                popup.show();
            };

            this.date_input = function (caption, callback) {
                var popup = instantiate_modal(caption, "Дата оплаты", DateInputModalPopup);

                function handle(success) {
                    var data = popup.get_data();
                    popup.dispose();
                    callback($.extend({}, data, {success: success}));
                }

                popup.create_controls();
                popup.set_buttons({
                    ok: function () {
                        handle(true);
                    },
                    cancel: function () {
                        handle(false);
                    }
                });
                popup.show();
            };
        }

        return UIManager;
    }
);
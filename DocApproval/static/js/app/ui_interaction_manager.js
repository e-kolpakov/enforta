/*global define*/
define(
    ['app/modal_popup'],
    function (modal_popup_module_exports) {
        var BasicPopupClass = modal_popup_module_exports.basic_popup_class;
        var modal_buttons_config = modal_popup_module_exports.buttons_config;

        function UIManager() {
            var that = this;

            function instantiate_modal(caption, message, dlg_class) {
                var DialogClass = dlg_class || BasicPopupClass;
                var popup = new DialogClass();
                popup.set_content(message);
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
            this.confirmation = function (question, callback, caption) {
                var eff_caption = caption || "Подтверждение";
                var popup = instantiate_modal(eff_caption, question);
                popup.set_buttons({
                    ok: function () {
                        callback(true);
                    },
                    cancel: function () {
                        popup.dispose();
                        callback(false);
                    }
                });
                popup.show();
            };
            this.input = function (caption, callback) {
                var comment = prompt(caption);
                return {
                    success: !!comment, // mnemonic boolean coercion
                    comment: comment
                };
            };
            this.error = function (message) {
                that.message(message, "Ошибка");
            };
        }

        return UIManager;
    }
);
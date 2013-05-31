/*global define*/
define(
    ['app/modal_popup'],
    function (ModalPopup) {
        function UIManager() {
            var that = this;
            var popup = new ModalPopup([]);
            this.message = function (message, caption) {
                var eff_caption = caption || "Сообщение";
                popup.set_content(message);
                popup.set_header(eff_caption);
                popup.show();
            };
            this.confirmation = function (question) {
                return confirm(question);
            };
            this.input = function (caption, callback) {
                var comment = prompt(caption);
                return {
                    success: !!comment, // mnemonic boolean coercion
                    comment: comment
                };
            };
            this.error = function (message) {
                that.message(message);
            };
        }

        return UIManager;
    }
);
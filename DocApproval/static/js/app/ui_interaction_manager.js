/*global define*/
define(
    ['jquery'],
    function ($) {
        function UIManager() {
            var that = this;
            this.message = function (message) {
                alert(message);
            };
            this.confirmation = function (question) {
                return confirm(question);
            };
            this.error = function (message) {
                that.message(message);
            };
        }

        return UIManager;
    }
);
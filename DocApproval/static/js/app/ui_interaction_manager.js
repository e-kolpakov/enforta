/*global define*/
define([], function () {
    var ui_manager = {
        message: function (message) {
            alert(message);
        },
        confirmation: function (question) {
            return confirm(question);
        }
    };

    return ui_manager;
});
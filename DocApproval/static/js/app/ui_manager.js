var UiManager = (function () {
    return {
        message: function (message) {
            alert(message);
        },
        confirmation: function (question) {
            return confirm(question);
        }
    };
}());
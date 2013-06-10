/*global define*/
define(
    [],
    function () {
        // Maybe it's worth adding robust server-side logging? Anyway, it's not even a to do.
        function Logger() {
            this.log = function (message) {
                if (console && console.log) {
                    console.log(message);
                }
            };
        }

        return Logger;
    }
);
/*global define*/
define(
    ['jquery', 'app/dispatcher', 'app/services/logger'],
    function ($, Dispatcher, Logger) {
        "use strict";

        var logger = new Logger();

        function mass_approve() {
            logger.log("approve");
        }

        function mass_reject() {
            logger.log("reject");
        }

        Dispatcher.notify_behavior('mass-approve', {'click': mass_approve});
        Dispatcher.notify_behavior('mass-reject', {'click': mass_reject});
    }
);
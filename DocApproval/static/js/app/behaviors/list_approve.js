/*global define*/
define(
    ['jquery', 'app/dispatcher', 'app/services/ui_interaction_manager', 'app/services/logger', 'app/messages'],
    function ($, Dispatcher, UIManager, Logger, messages) {
        "use strict";

        var logger = new Logger();
        var ui_manager = new UIManager();

        function get_comments(message, callback) {
            ui_manager.input(message, callback);
        }

        function get_request_pks(button) {
            var table = $(button).parents(".dataTables_wrapper").find("table.dataTable");
            var checkboxes = $(table).find("input[type='checkbox'].row-checkbox:checked");
            return $.map(checkboxes, function (val, idx) {
                return $(val).val();
            });
        }

        function handle_action(button, action, comment) {
            var pks = get_request_pks(button);
            logger.log(action);
            logger.log(comment);
            logger.log(pks);
        }

        function mass_approve(event) {
            get_comments(messages.ActionMessages.confirm_approve, function (data) {
                if (data.success) {
                    handle_action(event.target, 'approve', data.comment);
                }
            });
        }

        function mass_reject(event) {
            get_comments(messages.ActionMessages.confirm_rejection, function (data) {
                if (data.success) {
                    handle_action(event.target, 'reject', data.comment);
                }
            });
        }

        Dispatcher.notify_behavior('mass-approve', {'click': mass_approve});
        Dispatcher.notify_behavior('mass-reject', {'click': mass_reject});
    }
);
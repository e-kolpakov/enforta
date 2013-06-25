/*global define*/
define(
    [
        'jquery',
        'app/dispatcher', 'app/services/ui_interaction_manager', 'app/services/ajax_communicator',
        'app/services/logger', 'app/messages'
    ],
    function ($, Dispatcher, UIManager, Communicator, Logger, Messages) {
        "use strict";

        var logger = new Logger();
        var ui_manager = new UIManager();
        var comm = new Communicator();

        function get_comments(message, callback) {
            ui_manager.input(message, callback);
        }

        function get_backend_url(element) {
            return $(element).attr('data-backend-url');

        }

        function get_request_pks(button) {
            var table = $(button).parents(".dataTables_wrapper").find("table.dataTable");
            var checkboxes = $(table).find("input[type='checkbox'].row-checkbox:checked");
            return $.map(checkboxes, function (val, idx) {
                return $(val).val();
            });
        }

        function handle_action(button, action, comment, backend_url) {
            var pks = get_request_pks(button);
            var data = JSON.stringify({
                action: action,
                request_pks: pks,
                parameters: { comment: comment }
            });
            var action_promise = comm.make_request({url: backend_url}, data);
            action_promise.done(function (response_data, textStatus, jqXHR) {
                if (response_data.success) {
                }
                if (response_data.errors) {
                    ui_manager.message(Messages.Common.errors_happened + response_data.errors.join("\n"));
                }
                $(button).trigger('reload.datatable');
            });

            action_promise.fail(function (jqXHR, textStatus, errorThrown) {
                ui_manager.error(errorThrown);
            });
        }

        function mass_approve(event) {
            var backend_url = get_backend_url(event.target);
            get_comments(Messages.ActionMessages.confirm_approve, function (data) {
                if (data.success) {
                    handle_action(event.target, 'approve', data.comment, backend_url);
                }
            });
        }

        function mass_reject(event) {
            var backend_url = get_backend_url(event.target);
            get_comments(Messages.ActionMessages.confirm_rejection, function (data) {
                if (data.success) {
                    handle_action(event.target, 'reject', data.comment, backend_url);
                }
            });
        }

        Dispatcher.notify_behavior('mass-approve', {'click.behaviors.list_approve': mass_approve});
        Dispatcher.notify_behavior('mass-reject', {'click.behaviors.list_approve': mass_reject});
    }
);
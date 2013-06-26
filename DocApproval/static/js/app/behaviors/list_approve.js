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

        var confirmation_messages = {
            'approve': Messages.ActionMessages.confirm_approve,
            'reject': Messages.ActionMessages.confirm_rejection
        };

        var success_messages = {
            'approve': Messages.ActionMessages.approve_successful,
            'reject': Messages.ActionMessages.rejection_successful
        }

        function handle_action(button, action, request_pk, parameters) {
            var backend_url = $(button).data('backendUrl');

            var data = JSON.stringify({
                action: action,
                request_pk: request_pk,
                parameters: { comment: parameters.comment, on_behalf_of: parameters.on_behalf_of }
            });
            var action_promise = comm.make_request({url: backend_url}, data);
            action_promise.done(function (response_data, textStatus, jqXHR) {
                if (response_data.success) {
                    $(button).trigger('reload_datatable.behaviors.list_approve');
                    ui_manager.message(success_messages[action]);
                }
                if (response_data.errors) {
                    ui_manager.error(Messages.Common.errors_happened + response_data.errors.join("\n"));
                }
            });

            action_promise.fail(function (jqXHR, textStatus, errorThrown) {
                ui_manager.error(errorThrown);
            });
        }

        function list_approve_action(event) {
            var action_code = $(event.target).data('actionCode');
            var request_pk = $(event.target).data('requestPk');
            var confirmation = confirmation_messages[action_code] || Messages.Common.generic_action_confirmation;
            ui_manager.input(confirmation, action_code, request_pk, function (data) {
                if (data.success) {
                    handle_action(event.target, action_code, request_pk, data);
                }
            });
        }

        Dispatcher.notify_behavior('list-approve-action', {'click': list_approve_action});
    }
);
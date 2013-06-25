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
        }

        function handle_action(button, action, comment) {
            var backend_url = $(button).data('backendUrl');
            var request_pk = $(button).data('requestPk');
            var data = JSON.stringify({
                action: action,
                request_pk: request_pk,
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

        function list_approve_action(event) {
            var action_code = $(event.target).data('actionCode');
            var confirmation = confirmation_messages[action_code] || Messages.Common.generic_action_confirmation;
            ui_manager.input(confirmation, function (data) {
                if (data.success) {
                    handle_action(event.target, action_code, data.comment);
                }
            });
        }

        Dispatcher.notify_behavior('list-approve-action', {'click': list_approve_action});
    }
);
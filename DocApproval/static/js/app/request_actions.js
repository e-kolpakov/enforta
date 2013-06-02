/*global globals, define*/
define(
    ['jquery', 'app/ui_interaction_manager', 'app/ajax_communicator', 'app/ui_action_handlers'],
    function ($, UIManager, Communicator, handlers) {
        "use strict";

        var Messages = {
            action_failed: "Не удалось совершить действие: "
        };

        // TODO: add real logging/notifying
        // TODO: use injection instead of copy-pasting
        var logger = function (msg) {
            if (console && console.log) {
                console.log(msg);
            }
        };

        var ui_manager = new UIManager();

        var Comm = function (csrf, actions_backend_url) {
            var ajax_comm = new Communicator(csrf);

            this.post_action = function (action, request_id, parameters) {
                var data = JSON.stringify({
                    'action': action,
                    'request_pk': request_id,
                    'parameters': parameters
                });
                return ajax_comm.make_request({url: actions_backend_url, data: data});
            };
        };

        var ActionHandler = function (communicator) {
            var ui_handlers = {};
            ui_handlers[handlers.ActionCodes.TO_APPROVAL] = handlers.ToApprovalActionHandler;
            ui_handlers[handlers.ActionCodes.TO_PROJECT] = handlers.ToProjectActionHandler;
            ui_handlers[handlers.ActionCodes.APPROVE] = handlers.ApproveActionHandler;
            ui_handlers[handlers.ActionCodes.REJECT] = handlers.RejectActionHandler;

            function reload_if_needed(force, ask) {
                if (force) {
                    location.reload();
                } else {
                    if (ask) {
                        ui_manager.confirmation("Перезагрузить страницу?", function (reload) {
                            if (reload) {
                                location.reload();
                            }
                        });
                    }
                }
            }

            function handle_callback(action, request_id, action_handler_result) {
                var post_action = action_handler_result.post_action;
                var parameters = action_handler_result.data;

                if (post_action) {
                    var action_promise = communicator.post_action(action, request_id, parameters);
                    action_promise.done(function (response_data, textStatus, jqXHR) {
                        if (response_data.success) {
                            var response = response_data.response;
                            logger(response);
                            reload_if_needed(response.reload_require, response.reload_ask);
                        } else {
                            ui_manager.message(Messages.action_failed + response_data.errors.join("\n"));
                        }
                    });

                    action_promise.fail(function (jqXHR, textStatus, errorThrown) {
                        ui_manager.error(errorThrown);
                    });
                }
            }

            this.handle = function (action, request_id) {
                logger("Handling action " + action + " on request " + request_id);
                if (ui_handlers[action]) {
                    var handler = new ui_handlers[action](request_id);
                    handler.handle(handle_callback);
                }
            };
        };

        $.fn.request_actions_panel = function (request_id, options) {
            var actions_backend_url = options.actions_backend_url;
            var csrf = options.csrftoken || $.cookie('csrftoken');

            var comm = new Comm(csrf, actions_backend_url);
            var action_handler = new ActionHandler(comm);

            $('tr.action-row', this).click(function (e) {
                var action = $(this).find(".action-code-hidden").val();
                action_handler.handle(action, request_id);
            });
        };
    }
);

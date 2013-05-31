/*global globals, define*/
define(
    ['jquery', 'app/ui_interaction_manager', 'app/ajax_communicator', 'extend'],
    function ($, UIManager, Communicator, extend) {
        "use strict";

        // Always keep in sync with codes in request_management/actions.py
        var ActionCodes = {
            TO_APPROVAL: 'to_approval',
            TO_PROJECT: 'to_project',
            APPROVE: 'approve',
            REJECT: 'reject'
        };

        var Messages = {
            action_failed: "Не удалось совершить действие: ",
            confirm_to_negotiation: 'Перевод заявки в состояние "В согласовании" начнет процесс утверждения. Продолжить?',
            confirm_to_project: 'Перевод заявки в состояние "Проект" приведет к остановке текущего процесса утверждения. Продолжить?',
            confirm_approve: "Утвердить заявку?",
            confirm_rejection: "Отклонить заявку?"
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

        function BaseActionHandler() {
        }

        BaseActionHandler.prototype = {
            validate_callback: function (callback_to_validate) {
                return (callback_to_validate && typeof callback_to_validate === "function");
            },

            process_action: function (callback) {
                logger("Should be overridden in child classes");
                callback({post_action: false});
            },

            handle: function (callback) {
                if (this.validate_callback(callback)) {
                    this.process_action(callback);
                }
            }
        };

        function StatusActionHandler() {
        }

        var ToApprovalActionHandler = function (request_id) {
            var action_code = ActionCodes.TO_APPROVAL;
            this.process_action = function (callback) {
                ui_manager.confirmation(Messages.confirm_to_negotiation, function (is_confirmed) {
                    callback(action_code, request_id, {post_action: is_confirmed});
                });
            };
        };
        var ToProjectActionHandler = function (request_id) {
            var action_code = ActionCodes.TO_PROJECT;
            this.process_action = function (callback) {
                ui_manager.confirmation(Messages.confirm_to_project, function (is_confirmed) {
                    callback(action_code, request_id, {post_action: is_confirmed});
                });
            };
        };

        var ApproveActionHandler = function (request_id) {
            var action_code = ActionCodes.APPROVE;
            this.process_action = function (callback) {
                var confirm_and_get_comment = ui_manager.input(Messages.confirm_approve);
                callback(action_code, request_id, {
                    post_action: confirm_and_get_comment.success,
                    data: {
                        comment: confirm_and_get_comment.comment
                    }
                });
            };
        };

        var RejectActionHandler = function (request_id) {
            var action_code = ActionCodes.REJECT;
            this.process_action = function (callback) {
                var confirm_and_get_comment = ui_manager.input(Messages.confirm_rejection);
                callback(action_code, request_id, {
                    post_action: confirm_and_get_comment.success,
                    data: {
                        comment: confirm_and_get_comment.comment
                    }
                });
            };
        };

        extend(ToApprovalActionHandler, BaseActionHandler);
        extend(ToProjectActionHandler, BaseActionHandler);
        extend(ApproveActionHandler, BaseActionHandler);
        extend(RejectActionHandler, BaseActionHandler);

        var ActionHandler = function (communicator) {
            var ui_handlers = {};
            ui_handlers[ActionCodes.TO_APPROVAL] = ToApprovalActionHandler;
            ui_handlers[ActionCodes.TO_PROJECT] = ToProjectActionHandler;
            ui_handlers[ActionCodes.APPROVE] = ApproveActionHandler;
            ui_handlers[ActionCodes.REJECT] = RejectActionHandler;

            function need_reload(force, ask) {
                return force || (ask && ui_manager.confirmation("Перезагрузить страницу?"));
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
                            if (need_reload(response.reload_require, response.reload_ask)) {
                                location.reload();
                            }
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

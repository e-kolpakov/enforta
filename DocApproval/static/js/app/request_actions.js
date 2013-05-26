/*global globals*/
(function ($) {
    "use strict";

    // Always keep in sync with codes in request_management/actions.py
    var ActionCodes = {
        TO_APPROVAL: 'to_approval',
        TO_PROJECT: 'to_project'
    };

    var Messages = {
        action_failed: "Не удалось совершить действие: ",
        confirm_to_negotiation: 'Перевод заявки в состояние "В согласовании" начнет процесс утверждения. Продолжить?',
        confirm_to_project: 'Перевод заявки в состояние "Проект" приведет к остановке текущего процесса утверждения. Продолжить?'
    };

    // TODO: add real logging/notifying
    // TODO: use injection instead of copy-pasting
    var logger = function (msg) {
        if (console && console.log) {
            console.log(msg);
        }
    };
    var ui_notifier = {
        message: function (message) {
            alert(message);
        },
        confirmation: function (question) {
            return confirm(question);
        }
    };

    var Communicator = function (csrf, actions_backend_url) {
        var that = this;
        if (csrf) {
            $.ajaxSetup({
                beforeSend: function (xhr) {
                    xhr.setRequestHeader("X-CSRFToken", csrf);
                }
            });
        }

        this.actions_backend_url = actions_backend_url;
        this.post_action = function (action, request_id, parameters) {
            var ajax_call = $.ajax({
                type: 'POST',
                url: that.actions_backend_url,
                dataType: 'json',
                data: JSON.stringify({
                    'action': action,
                    'request_pk': request_id,
                    'parameters': parameters
                })
            });
            return ajax_call.promise();
        };
    };

    function BaseActionHandler() {
        this.handle = function () {
            logger("In BaseActionHandler.handle");
            return {post_action: false};
        };
    }

    var ToApprovalActionHandler = function () {
        this.handle = function () {
            return {post_action: ui_notifier.confirmation(Messages.confirm_to_negotiation)};
        };
    };
    var ToProjectActionHandler = function () {
        this.handle = function () {
            return {post_action: ui_notifier.confirmation(Messages.confirm_to_project)};
        };
    };

    ToApprovalActionHandler.prototype = new BaseActionHandler();
    ToProjectActionHandler.prototype = new BaseActionHandler();

    var ActionHandler = function (communicator) {
        var ui_handlers = {};
        ui_handlers[ActionCodes.TO_APPROVAL] = new ToApprovalActionHandler();
        ui_handlers[ActionCodes.TO_PROJECT] = new ToProjectActionHandler();

        function need_reload(force, ask) {
            return force || (ask && ui_notifier.confirmation("Перезагрузить страницу?"));
        }

        this.handle = function (action, request_id) {
            logger("Handling action " + action + " on request " + request_id);
            var post_action = true;
            if (ui_handlers[action]) {
                var handler = ui_handlers[action];
                var ui_result = handler.handle();
                post_action &= ui_result.post_action;
            }
            if (!post_action) {
                return;
            }
            var action_promise = communicator.post_action(action, request_id, { test: 'test' });
            action_promise.done(function (response_data, textStatus, jqXHR) {
                if (response_data.success) {
                    var response = response_data.response;
                    logger(response);
                    if (need_reload(response.reload_require, response.reload_ask)) {
                        location.reload();
                    }
                } else {
                    ui_notifier.message(Messages.action_failed + response_data.errors.join("\n"));
                }
            });

            action_promise.fail(function (jqXHR, textStatus, errorThrown) {
                ui_notifier.message(errorThrown);
            });
        };
    };

    $.fn.request_actions_panel = function (request_id, options) {
        var actions_backend_url = options.actions_backend_url;
        var csrf = options.csrftoken || $.cookie('csrftoken');

        var comm = new Communicator(csrf, actions_backend_url);
        var action_handler = new ActionHandler(comm);

        $('tr.action-row', this).click(function (e) {
            var action = $(this).find(".action-code-hidden").val();
            action_handler.handle(action, request_id);
        });
    };
}(window.jQuery));

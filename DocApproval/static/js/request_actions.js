/*global globals*/
(function ($) {
    "use strict";

    // TODO: add real logging/notifying
    // TODO: use injection instead of copy-pasting
    var logger = function (msg) {
        if (console && console.log) {
            console.log(msg);
        }
    };
    var ui_notifier = alert;

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
        this.post_action = function (action, parameters) {
            var ajax_call = $.ajax({
                type: 'POST',
                url: that.actions_backend_url,
                dataType: 'json',
                data: JSON.stringify({
                    'action': action,
                    'parameters': parameters
                })
            });
            return ajax_call.promise();
        };
    };

    var ActionHandler = function (communicator) {
        this.handle = function (action, request_id) {
            logger("Handling action " + action + " on request " + request_id);
            communicator.post_action(action, {request_id: request_id});
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

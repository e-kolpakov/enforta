/*global define, globals*/
define(
    [
        'jquery',
        'app/dispatcher', 'app/services/ajax_communicator', 'app/services/ui_interaction_manager',
        'app/services/logger', 'app/messages'
    ],
    function ($, Dispatcher, Communicator, UIManager, Logger, Messages) {
        "use strict";
        /* behavior parameters:
         'data-behavior': 'notifications-display',
         'data-refresh-interval': interval,
         'data-display-id': display element id
         */
        var notifications_backend_url = globals.notifications_backend;
        var no_new_messages = globals.static_root + "img/icons/no_new_messages.png";
        var new_messages = globals.static_root + "img/icons/new_messages.png";

        var display_id_attr = 'display-id';
        var highlight_class = 'highlight';

        var any = function (array, predicate) {
            return $.grep(array, predicate).length > 0;
        };

        var getGuid = function () {
            return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
                var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
                return v.toString(16);
            });
        }

        var comm = new Communicator(),
            logger = new Logger(),
            ui_manager = new UIManager();

        function currentUtcTimestamp() {
            var date = new Date();
            var utcMicrosecondsSinceEpoch = date.getTime() + date.getTimezoneOffset();
            return Math.round(utcMicrosecondsSinceEpoch / 1000);
        }

        function make_notification_row($display, data, highlight) {
            var time = new Date(data.event_timestamp * 1000 + new Date().getTimezoneOffset() * 60000);
            var disp_time = time.toLocaleDateString() + " " + time.toLocaleTimeString();

            var div = $("<div></div>").addClass("notification-message").insertAfter($display);
            var div_head = $("<div></div>").addClass("notification-message-head").appendTo(div);
            $("<span></span>").addClass("notification-message-event-type").text(data.event_type_name).appendTo(div_head);
            $("<span></span>").addClass("notification-message-timestamp").text(disp_time).appendTo(div_head);
            var request_data = $("<div></div>").addClass("notification-request-data").appendTo(div);
            $("<a></a>").attr('href', data.request_url).text(data.request_name).appendTo(request_data);

            if (data.notification_ui_dismissed === false) {
                div.addClass(highlight_class);
            }
            return div;
        }

        function make_display($control) {
            var $display = $("<div></div>").addClass("notification-ui-display").attr('id', getGuid());
            $("<div></div>").addClass("notification-ui-display-title").appendTo($display).
                text(Messages.NotificationMessages.display_title);
            $("<div></div>").addClass("notification-ui-display-body").appendTo($display);
            var control_offset = $control.offset();
            $display.offset({
                top: control_offset.top + $control.height() + 10,
                left: control_offset.left - 250 + $control.width() / 2
            });
            $display.click(function(event){ event.stopPropagation(); });
            $("body").append($display);
            return $display;
        }

        function get_display($control) {
            return $("#"+$control.data(display_id_attr));
        }

        function handleDataLoad($control, response) {
            if (response.success) {
                logger.log(response.data.notifications);
                var notifications = response.data.notifications;

                if (any(notifications, function (elem) {
                    return elem.notification_ui_dismissed === false;
                })) {
                    setIcon($control, new_messages);
                }

                var $display = get_display($control);
                var $insert_marker = $(".notification-ui-display-body", $display);
                for (var i=0; i<notifications.length; i++) {
                    make_notification_row($display, notifications[i]).prependTo($insert_marker);
                }
            } else {
                ui_manager.error(response.errors.join("\n"));
            }
        }

        function handleDataLoadFailure($control, errorThrown) {
            var interval = $control.data('refresh-interval');
            if (interval) {
                clearInterval(interval);
            }
            ui_manager.error(Messages.NotificationMessages.notification_load_failure);
        }

        function init_notification_ui(event) {
            var $control = $(event.target);
            var $display = make_display($control);

            $("a", $control).click(function(event) {
                event.preventDefault();
                anchor_click($control);
                return false;
            });

            $control.data(display_id_attr, $display.attr('id'));
        }

        function load_initial_notification_data(event) {
            var $control = $(event.target);

            var data_promise = comm.make_request(
                { url: notifications_backend_url, type: 'GET'},
                {}
            );

            data_promise.done(function (data, textStatus, jqXHR) {
                handleDataLoad($control, data);
            });
            data_promise.fail(function (jqXHR, textStatus, errorThrown) {
                handleDataLoadFailure($control, errorThrown);
            });
        }

        function load_new_notifications(event) {
            var $control = $(event.target);

            var data_promise = comm.make_request(
                { url: notifications_backend_url, type: 'GET'},
                { timestamp: currentUtcTimestamp() - globals.notifications_poll_frequency }
            );

            data_promise.done(function (data, textStatus, jqXHR) {
                handleDataLoad($control, data);
            });
            data_promise.fail(function (jqXHR, textStatus, errorThrown) {
                handleDataLoadFailure($control, errorThrown);
            });
        }

        function anchor_click($control) {
            var $display = get_display($control);
            $("body").on('click.behaviors.notifications', function(event){
                $display.hide();
                $("body").unbind('click.behaviors.notifications');
                $("."+highlight_class).removeClass(highlight_class);
            });
            $display.show();
            setIcon($control, no_new_messages);
        }

        function setIcon($control, icon){
            $("a img", $control).attr('src', icon);
        }

        Dispatcher.notify_behavior(
            'notifications-display',
            {
                'init.behaviors.notifications': init_notification_ui,
                'load_initial.behaviors.notifications': load_initial_notification_data,
                'load_new.behaviors.notifications': load_new_notifications
//                'click.behaviors.notifications': anchor_click
            }
        );
    }
);
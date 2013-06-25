/*global define*/
define(
    ['jquery'],
    function ($) {
        'use strict';
        var behaviors = {};

        var Dispatcher = {
            behavior_attribute: 'data-behavior',

            notify_element: function (element) {
                var behavior = $(element).attr(Dispatcher.behavior_attribute);
                if (behaviors[behavior]) {
                    for (var event in behaviors[behavior]) {
                        if (!behaviors[behavior].hasOwnProperty(event)) continue;
                        var event_handlers = behaviors[behavior][event];
                        for (var i = 0; i < event_handlers.length; i++) {
                            $(element).on(event, event_handlers[i]);
                        }
                    }
                }
            },

            notify_behavior: function (behavior_name, behavior_events) {
                if (!behaviors[behavior_name]) {
                    behaviors[behavior_name] = {};
                }
                var behavior = behaviors[behavior_name];
                for (var event in behavior_events) {
                    if (!behavior_events.hasOwnProperty(event)) continue;
                    if (!behavior[event]) {
                        behavior[event] = [];
                    }
                    behavior[event].push(behavior_events[event]);
                }
            }
        };

        return Dispatcher;
    }
);
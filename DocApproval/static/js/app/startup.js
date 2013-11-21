/*global define, globals*/
define(
    ['jquery', 'app/dispatcher', 'jquery-ui', 'app/widgets/wrapped_datepicker'],
    function ($, Dispatcher) {
        globals.notifications_poll_frequency = 10; // in seconds
        $(function () {
            $(".datepicker").wrapped_datepicker({
                showButtonPanel: true
            });

            var messages_menu = $("#messages_menu");
            Dispatcher.notify_element(messages_menu);
            messages_menu.trigger('init');
            messages_menu.trigger('load_initial');
            var interval = setInterval(function () {
                messages_menu.trigger('load_new');
            }, globals.notifications_poll_frequency * 1000);
            messages_menu.data('refresh-interval', interval);
        });
    }
);
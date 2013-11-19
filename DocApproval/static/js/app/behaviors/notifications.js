/*global define, globals*/
define(
    [
        'jquery',
        'app/dispatcher', 'app/services/ajax_communicator', 'app/services/ui_interaction_manager',
        'app/services/logger', 'app/messages'
    ],
    function ($, Dispatcher, Communicator, UIManager, Logger, Messages) {
        var notifications_backend = globals.notifications_backend;

        var comm = new Communicator(),
            logger = new Logger(),
            ui_manager = new UIManager();
    }
);
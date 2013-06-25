/*global define*/
define(
    [
        'jquery',
        'app/dispatcher', 'app/services/ajax_communicator',
        'app/services/logger', 'app/messages'
    ],
    function ($, Dispatcher, Communicator, Logger, Messages) {
        //cache should really contain single element, but just for the sake of extensibility it is capable of more
        var impersonations_cache = {};

        function load_impersonations(event) {

        }

        Dispatcher.notify_behavior(
            'select-impersonation-for-request',
            {'init_control.behaviors.impersonation_list': load_impersonations}
        );
    }
);
/*global define*/
define(
    [
        'jquery',
        'app/dispatcher', 'app/services/ajax_communicator', 'app/services/ui_interaction_manager',
        'app/services/logger', 'app/messages'
    ],
    function ($, Dispatcher, Communicator, UIManager, Logger, Messages) {
        "use strict";
        /* behavior parameters:
         'data-behavior': 'list-approve-action',
         'data-action-code': code,
         'data-request-pk': pk
         */

        // keep this in sync with url_naming/profile.py
        // both leading AND trailing slashes required
        var impersonations_backend = "/profile/impersonations/request/";

        var comm = new Communicator(),
            logger = new Logger(),
            ui_manager = new UIManager();

        function get_behavior_parameters($control) {
            return {
                url: impersonations_backend,
                code: $control.data('actionCode'),
                request_pk: $control.data('requestPk')
            };
        }

        function set_control_data($control, data) {
            $control.empty();
            var impersonated_id;
            for (impersonated_id in data) {
                if (data.hasOwnProperty(impersonated_id)) {
                    var impersonated_name = data[impersonated_id];
                    $("<option></option>").attr("value", impersonated_id).text(impersonated_name).appendTo($control);
                }
            }
        }

        function enable_control($control) {
            $control.removeAttr('disabled');
        }

        function load_impersonations(event) {
            var $control = $(event.target);
            var parameters = get_behavior_parameters($control);
            var impersonations_promise = comm.make_request(
                { url: parameters.url },
                { code: parameters.code, request_pk: parameters.request_pk }
            );
            impersonations_promise.done(function (data, textStatus, jqXHR) {
                logger.log(data);
                if (data.success) {
                    set_control_data($control, data.impersonations);
                    enable_control($control);
                } else {
                    ui_manager.error(data.errors.join("\n"));
                }
            });
            impersonations_promise.fail(function (jqXHR, textStatus, errorThrown) {
                ui_manager.error(errorThrown);
            });
        }

        Dispatcher.notify_behavior(
            'select-impersonation-for-request',
            {'init_control.behaviors.impersonation_list': load_impersonations}
        );
    }
);
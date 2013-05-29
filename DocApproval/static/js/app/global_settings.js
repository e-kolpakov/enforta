/*global globals, define*/
define(
    ['jquery', 'libjquery/jquery.ui.datepicker-ru'],
    function ($) {
        "use strict";
        var settings = {
            datepicker_defaults: {
                auto_size: false,
                constrainInput: true,
                showOtherMonths: true,
                selectOtherMonths: true,
                showOn: 'both',
                buttonImage: globals.static_root + '/img/calendar.png'
            }
        };

        $.extend(settings.datepicker_defaults, $.datepicker.regional.ru);
        $.datepicker.setDefaults(settings.datepicker_defaults);
    }
);
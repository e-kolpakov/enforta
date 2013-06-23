/*global define, globals*/

define(
    ['jquery', 'jquery-ui'],
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

        $.fn.wrapped_datepicker = function (options) {
            $(this).wrap("<div class='datepicker-wrapper'/>").datepicker(options);
            if ($(this).attr('id')) {
                $(this).parents(".datepicker-wrapper").attr({id: $(this).attr('id') + '-wrapper'});
            }
        };
    }
);
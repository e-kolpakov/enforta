"use strict";
(function ($) {
    var settings = {
        datepicker_defaults: {
            auto_size: false,
            constrainInput: true,
            showOtherMonths: true,
            selectOtherMonths: true,
            showOn: 'both'

        }
    };

    $.extend(settings.datepicker_defaults, $.datepicker.regional["ru"]);
    $.datepicker.setDefaults(settings.datepicker_defaults);
}(window.jQuery));
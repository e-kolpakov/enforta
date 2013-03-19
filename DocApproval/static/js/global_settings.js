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

    $.extend(settings.datepicker_defaults, $.datepicker.regional[ "ru" ]);
    $.datepicker.setDefaults(settings.datepicker_defaults);

    if (console) {
        console.log("Global settings initialized");
        console.log(settings.datepicker_defaults);
        console.log($.datepicker.regional[ "ru" ]);
    }
})(jQuery);
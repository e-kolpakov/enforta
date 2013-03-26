(function ($) {
    "use strict";
    $.fn.wrapped_datepicker = function (options) {
        $(this).datepicker(options).end().wrap("<div class='datepicker-wrapper'/>");
        if ($(this).attr('id')) {
            $(this).parents(".datepicker-wrapper").attr({id: $(this).attr('id') + '-wrapper'});
        }
    };
}(window.jQuery));
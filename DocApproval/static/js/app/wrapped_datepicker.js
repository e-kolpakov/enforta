/*global define*/

define(
    ['jquery', 'jquery-ui', 'app/global_settings'],
    function ($) {
        "use strict";
        $.fn.wrapped_datepicker = function (options) {
            $(this).wrap("<div class='datepicker-wrapper'/>").datepicker(options);
            if ($(this).attr('id')) {
                $(this).parents(".datepicker-wrapper").attr({id: $(this).attr('id') + '-wrapper'});
            }
        };
    }
);
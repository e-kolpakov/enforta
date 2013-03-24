(function ($) {
    "use strict";
    $.fn.datepicker_ui_button = function (options) {
        $(this).datepicker(options).next('button').text('').button({icons: {primary : 'ui-icon-calendar'}});
    };
}(window.jQuery));
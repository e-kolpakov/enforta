/*global define*/

define(['jquery'],
    function ($) {
        $.fn.error_handling_form = function (options) {
            var error_popup_selector = options.error_popup_selector || "div.field_errors_list";
            var field_errors_selector = options.field_errors_selector || ".field_errors";

            this.find(field_errors_selector).parent("label").hover(
                function () {
                    $(this).children(error_popup_selector).show();
                },
                function () {
                    $(this).children(error_popup_selector).hide();
                }
            );

            $(error_popup_selector).click(function () {
                $(this).hide();
            });
        }
    }
);
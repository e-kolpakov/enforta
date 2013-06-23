/*global define, page_data*/
define(['jquery', 'app/forms/forms'], function ($) {
    function get_page_data() {
        return page_data; // assuming global page-specific page_data variable
    }

    var config = get_page_data();

    return function () {
        $(function () {
            $(config.target).error_handling_form({
                error_popup_selector: config.error_popup_selector,
                field_errors_selector: config.field_errors_selector
            });
        });
    };
});
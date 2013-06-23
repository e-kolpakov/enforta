/*global define, page_data*/
define(['jquery', 'app/ajax_configurable_datatables'], function ($) {
    function get_page_data() {
        return page_data; // assuming global page-specific page_data variable
    }

    var options = get_page_data();

    return function () {
        $(function () {
            $(options.target).ajaxConfigurableDatatables(options);
        });
    };
});

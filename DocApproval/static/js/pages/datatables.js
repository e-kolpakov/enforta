/*global define, page_data*/
define(['jquery', 'app/ajax_configurable_datatables'], function ($) {
    function get_page_data() {
        return page_data; // assuming global page-specific page_data variable
    }

    var config = get_page_data();
    var options = {
        data_url: config.data_url,
        config_url: config.config_url
    };
    if (config.extra_server_params) {
        options.extra_server_params = config.extra_server_params;
    }
    if (config.search_form) {
        options.search_form = config.search_form;
        options.search_form_prefix = config.search_form_prefix;
    }

    return function () {
        $(function () {
            $(config.target).ajaxConfigurableDatatables(options);
        });
    };
});

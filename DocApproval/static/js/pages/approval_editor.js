/*global define, page_data*/
define(['jquery', 'app/approval_route_editor'], function ($) {
    function get_page_data() {
        return page_data; // assuming global page-specific page_data variable
    }

    var config = get_page_data();

    return function () {
        $(function () {
            $(config.target).approval_route_editor(config.page_config, config.initial_data);
        });
    };
});

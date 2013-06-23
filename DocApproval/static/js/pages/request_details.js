/*global define, page_data*/

define(['jquery', 'app/request_actions/request_actions'], function ($) {
    function get_page_data() {
        return page_data;
    }

    var config = get_page_data();

    return function () {
        $(function () {
            $(config.target).request_actions_panel(config.request_id, config.config);
        });
    };
});
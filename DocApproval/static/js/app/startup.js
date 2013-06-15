/*global define*/
define(['jquery', 'jquery-ui', 'app/wrapped_datepicker'], function ($) {
    $(function () {
        $(".datepicker").wrapped_datepicker({
            showButtonPanel: true
        });
    });
});
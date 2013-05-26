/*global define*/
define(['jquery', 'jquery-ui', 'app/wrapped_datepicker'], function ($) {
    $("html").addClass('JS'); // allows to hide the content to be shown by JS while the page is loading
    $(function () {
        $(".datepicker").wrapped_datepicker();
    });
});
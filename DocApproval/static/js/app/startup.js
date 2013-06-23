/*global define*/
define(['jquery', 'jquery-ui', 'app/widgets/wrapped_datepicker'], function ($) {
    $(function () {
        $(".datepicker").wrapped_datepicker({
            showButtonPanel: true
        });

        $("[data-behavior]").click(function () {
            alert(1);
        });
    });
});
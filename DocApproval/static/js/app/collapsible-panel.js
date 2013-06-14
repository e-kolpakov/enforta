/*global define*/
define(
    ['jquery'],
    function ($) {
        $(function () {
            $("div.collapsible-panel a.collapsible-toggle").click(function () {
                $("span.ui-icon", $(this)).toggleClass("ui-icon-triangle-1-s").toggleClass("ui-icon-triangle-1-n");
            });
        });
    }
);
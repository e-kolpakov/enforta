(function ($) {
    function restful_link_formatter(cellvalue, options, rowObject){
        return "<a href='" + options.colModel.url_base + "/" + options.rowId + "'>" + cellvalue + "</a>";
    }

    $.extend($.fn.fmatter, {
        restfullink: restful_link_formatter
    });
}(window.jQuery));
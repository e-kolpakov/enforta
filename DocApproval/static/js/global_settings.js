(function ($, globals) {
    "use strict";
    var settings = {
        datepicker_defaults: {
            auto_size: false,
            constrainInput: true,
            showOtherMonths: true,
            selectOtherMonths: true,
            showOn: 'both',
            buttonImage: globals.static_root + '/img/calendar.png'
        }
    };

    $.extend(settings.datepicker_defaults, $.datepicker.regional["ru"]);
    $.datepicker.setDefaults(settings.datepicker_defaults);

    var jqgrid_defaults = {
        autowidth: true,
        datatype: 'json',
        gridview: true, //not going to use tree, sub and inserting
        height: '100%',
        loadui: 'block',
        mtype: 'get',
        rowNum: 25,
        rowList: [10, 25, 50],
        jsonReader: {
            repeatitems: false,
            total: 'totalpages',
            records: 'totalrecords',
            root: 'data',
            cell: 'fields',
            id: 'pk'
        }
    };
    jQuery.extend(jQuery.jgrid.defaults, jqgrid_defaults);
}(window.jQuery, window.globals));
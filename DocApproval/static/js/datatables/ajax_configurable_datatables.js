/*globals $*/

(function ($) {
    function get_header_row(target) {
        var header = target.children('thead');
        if (header.length === 0) {
            header = $("<thead></thead>").appendTo(target);
        }
        var row = header.children('tr');
        if (row.length === 0) {
            row = $("<tr></tr>").appendTo(header);
        }
        return row;
    }

    function create_header(target, headers, headers_order) {
        var header_row = get_header_row(target);
        for (var i = 0; i < headers_order.length; i++) {
            var key = headers_order[i];
            if (!headers.hasOwnProperty(key))
                continue;
            $("<th></th>").text(headers[key]).appendTo(header_row);
        }
    }

    function create_table(target, table_options) {
        target.dataTable(table_options);
    }

    function get_column_config(data) {
        var order = data.column_order;
        var links = data.links;
        var result = [];
        for (var i = 0; i < order.length; i++) {
            var col = order[i];
            var column = {'mData': col, 'sName': col};
            if (links.hasOwnProperty(col)) {
                var base_url = links[col];
                column['mRender'] = CustomColumnRenderersFactory.createEntityLinkRenderer(base_url);
            }
            result.push(column);
        }
        return result;
    }

    var CustomColumnRenderersFactory = {
        createEntityLinkRenderer: function (base_url) {
            return function (data, type, full) {
                return "<a href='" + base_url + "/" + full['pk'] + "'>" + data + "</a>";
            }
        }
    };

    var default_options = {
        bProcessing: true,
        bServerSide: true,
        sServerMethod: 'POST'
    };

    $.fn.ajaxConfigurableDatatables = function (options) {
        var self = this;
        $.ajaxSetup({
            beforeSend: function (xhr) {
                xhr.setRequestHeader("X-CSRFToken", options.csrftoken);
            }
        });
        $.ajax({
            url: options.config_url,
            type: 'get',
            dataType: 'json',
            success: function (data) {
                var new_options = {
                    sAjaxSource: options.data_url,
                    aoColumns: get_column_config(data)
                };
                var effective_options = $.extend(default_options, new_options);
                create_header(self, data.columns, data.column_order);
                create_table(self, effective_options);
            }
        });
    };
}($));
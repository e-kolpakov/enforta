/*globals define*/
define(
    [
        'jquery', 'app/ajax_communicator',
        'datatables/jquery.dataTables', 'datatables/dt_bootstrap', 'datatables/datatables-ru'
    ],
    function ($, Communicator) {

        var html_helper = {
            _create_header: function (target) {
                var header = target.children('thead');
                if (header.length === 0) {
                    header = $("<thead></thead>").appendTo(target);
                }
                var row = header.children('tr');
                if (row.length === 0) {
                    row = $("<tr></tr>").appendTo(header);
                }
                return row;
            },

            make_header: function (target, headers, headers_order) {
                var header_row = this._create_header(target);
                for (var i = 0; i < headers_order.length; i++) {
                    var key = headers_order[i];
                    if (!headers.hasOwnProperty(key))
                        continue;
                    $("<th></th>").text(headers[key]).appendTo(header_row);
                }
            },

            add_caption: function (target, caption) {
                $("<caption></caption>").text(caption).appendTo(target);
            },

            create_table: function (target, table_options) {
                target.dataTable(table_options);
            }
        };


        var config_parser = function (options) {
            function get_column_config(data) {
                var order = data.column_order;
                var links = data.links;
                var result = [];
                for (var i = 0; i < order.length; i++) {
                    var col = order[i];
                    var column = {'mData': col, 'sName': col};
                    if (links.hasOwnProperty(col)) {
                        var link_spec = links[col];
                        column['mRender'] = CustomColumnRenderersFactory.createEntityLinkRenderer(link_spec);
                    }
                    result.push(column);
                }
                return result;
            }

            function transform_extra_params(extra_params) {
                var result = [];
                for (var key in extra_params) {
                    if (!extra_params.hasOwnProperty(key))
                        continue;
                    result.push({'name': key, 'value': extra_params[key]});
                }
                return result;
            }

            var default_options = {
                bProcessing: true,
                bServerSide: true,
                sServerMethod: 'POST'
            };

            return {
                parse_config: function (datables_config, datatables_options) {
                    var new_options = {
                        sAjaxSource: options.data_url,
                        aoColumns: get_column_config(datables_config),
                        aLengthMenu: [5, 10, 25, 50, 100]
                    };
                    if (options.extra_server_params) {
                        var extra_params = transform_extra_params(options.extra_server_params);
                        new_options['fnServerData'] = function (sSource, aoData, fnCallback) {
                            aoData.push.apply(aoData, extra_params);
                            $.getJSON(sSource, aoData, function (json) {
                                fnCallback(json)
                            });
                        }
                    }
                    return {
                        options: $.extend({}, default_options, new_options, datatables_options),
                        columns: datables_config.columns,
                        column_order: datables_config.column_order
                    }
                }
            }
        };

        var CustomColumnRenderersFactory = {
            createEntityLinkRenderer: function (link_spec) {
                return function (data, type, full) {
                    var base_url = link_spec.base_url || "";
                    var entity_key = link_spec.entity_key || 'pk';
                    var link_url = base_url + "/" + full[entity_key];
                    return "<a href='" + link_url + "'>" + data + "</a>";
                }
            }
        };

        $.fn.ajaxConfigurableDatatables = function (options, datatables_opts) {
            var self = this;
            var datatables_options = datatables_opts || {};
            var parser = config_parser(options);
            var comm = new Communicator(options.csrftoken);
            var promise = comm.make_request({url: options.config_url, type: 'GET'});

            promise.done(function (datatables_config, textStatus, jqXHR) {
                var config = parser.parse_config(datatables_config, datatables_options);
                html_helper.make_header(self, config.columns, config.column_order);
                if (options.caption) {
                    html_helper.add_caption(self, options.caption);
                }
                html_helper.create_table(self, config.options);
            });
        };
    }
);
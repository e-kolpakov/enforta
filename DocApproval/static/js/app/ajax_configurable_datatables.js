/*globals define*/
define(
    [
        'jquery', 'app/services/ajax_communicator', 'app/forms/request_search_form', 'app/dispatcher',
        'datatables/jquery.dataTables', 'datatables/dt_bootstrap', 'datatables/datatables-ru'
    ],
    function ($, Communicator, SearchForm, Dispatcher) {

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

            make_header: function (target, columns) {
                var header_row = this._create_header(target);
                for (var i = 0; i < columns.length; i++) {
                    var column = columns[i];
                    var cell = $("<th></th>").appendTo(header_row);
                    if (!column.checkbox_config) {
                        cell.text(column.name);
                    } else {
                        $("<input>").attr('type', 'checkbox').
                            addClass('dt-select-all').appendTo(cell).
                            click(function () {
                                var checked = $(this).is(':checked');
                                $("input.row-checkbox", $(this).parents(".dataTables_wrapper")).prop('checked', checked);
                            });
                    }
                }
            },

            add_caption: function (target, caption) {
                $("<caption></caption>").text(caption).appendTo(target);
            },

            create_table: function (target, table_options) {
                return target.dataTable(table_options);
            },

            set_buttons: function (target, buttons_config) {
                for (var btn_class in buttons_config) {
                    if (!buttons_config.hasOwnProperty(btn_class)) continue;
                    var btn_cfg = buttons_config[btn_class];
                    var btn = $("<button/>").addClass(btn_class).text(btn_cfg.caption).appendTo($(target));
                    if (btn_cfg.css_class) {
                        btn.addClass(btn_cfg.css_class);
                    }
                    if (btn_cfg.attributes) {
                        btn.attr(btn_cfg.attributes);
                    }
                    Dispatcher.notify_element(btn);
                }
            }
        };


        var config_parser = function (options) {
            function build_column_definition(col) {
                var column = !(col.checkbox_config)
                    ? {mData: col.column, sName: col.column}
                    : {mData: null, mRender: CustomColumnRenderersFactory.createCheckBoxRenderer(col.checkbox_config)};
                if (col.link_config) {
                    column['mRender'] = CustomColumnRenderersFactory.createEntityLinkRenderer(col.link_config);
                }
                if (col.is_calculated) {
                    column['bSortable'] = false;
                }
                return column;
            }

            function get_column_config(data) {
                var columns = data.columns;
                var result = [];
                for (var i = 0; i < columns.length; i++) {
                    var col = columns[i];
                    result.push(build_column_definition(col));
                }
                return result;
            }

            function transform_params(extra_params) {
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
                parse_config: function (datables_config, datatables_options, search_form) {
                    var new_options = {
                        aaSorting: [],
                        sAjaxSource: options.data_url,
                        aoColumns: get_column_config(datables_config),
                        aLengthMenu: [5, 10, 25, 50, 100]
                    };

                    new_options['fnServerData'] = function (sSource, aoData, fnCallback) {
                        if (options.extra_server_params) {
                            aoData.push.apply(aoData, transform_params(options.extra_server_params));
                        }
                        if (search_form) {
                            aoData.push.apply(aoData, transform_params(search_form.get_data()));
                        }
                        $.getJSON(sSource, aoData, function (json) {
                            fnCallback(json)
                        });
                    };

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
            },

            createCheckBoxRenderer: function (checkbox_spec) {
                return function (data, type, full) {
                    var entity_key = checkbox_spec.entity_key || 'pk';
                    return "<input type='checkbox' class='row-checkbox' value='" + full[entity_key] + "'/>";
                }
            }
        };

        $.fn.ajaxConfigurableDatatables = function (options, datatables_opts) {
            var self = this;
            var datatables_options = datatables_opts || {};
            var parser = config_parser(options);
            var comm = new Communicator(options.csrftoken);
            var config_promise = comm.make_request({url: options.config_url, type: 'GET'}, options.extra_config_params || {});
            var search_form = options.search_form ? new SearchForm(options.search_form, options.search_form_prefix) : null;

            config_promise.done(function (datatables_config, textStatus, jqXHR) {
                var config = parser.parse_config(datatables_config, datatables_options, search_form);
                html_helper.make_header(self, config.columns);
                if (options.caption) {
                    html_helper.add_caption(self, options.caption);
                }
                var oTable = html_helper.create_table(self, config.options);
                html_helper.set_buttons(self.parent(".dataTables_wrapper").find(".btns"), datatables_config.buttons);

                if (search_form) {
                    search_form.add_listener(function (data) {
                        oTable.fnDraw(false);
                    });
                }
            });
        };
    }
);
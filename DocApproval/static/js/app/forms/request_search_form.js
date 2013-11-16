/*global define*/
define(
    ['jquery'],
    function ($) {
        function SearchForm(form_selector, form_prefix) {
            var that = this;
            this.form = $(form_selector);
            this._listeners = [];
            this._fixed_data = {};

            function roll_fixed_data() {
                var filter_id;
                var fixed_filters = that._fixed_data;
                for (filter_id in fixed_filters) {
                    if (fixed_filters.hasOwnProperty(filter_id)) {
                        $("#" + filter_id, that.form).
                            val(fixed_filters[filter_id]).
                            addClass('uneditable-input').
                            attr('disabled', 'disabled');
                    }
                }
            }

            this.add_listener = function (listener_callback) {
                this._listeners.push(listener_callback);
            };

            this.get_data = function () {
                var result = {};
                $("input, textarea, select", this.form).each(function () {
                    var value = $(this).val();
                    if (value) {
                        result[$(this).prop("name")] = $(this).val();
                    }
                });
                return result;
            };

            this.clear = function () {
                $('input[type=text], textarea', this.form).val('');
                $('input[type=checkbox], input[type=radio]', this.form).prop('checked', false);
                $('select', this.form).prop('selectedIndex', 0);

                roll_fixed_data();
            };

            this.submit = function () {
                var i;
                var data = this.get_data();
                for (i = 0; i < this._listeners.length; i += 1) {
                    var callback = this._listeners[i];
                    callback(data);
                }
            };

            this.set_fixed_filters = function (fixed_filters) {
                this._fixed_data = fixed_filters;
                roll_fixed_data();
            };

            $(document).ready(function () {
                $("button.search-btn", that.form).click(function (e) {
                    e.preventDefault();
                    that.submit();
                    return false;
                });
                $("button.reset-btn", that.form).click(function (e) {
                    e.preventDefault();
                    that.clear();
                    return this;
                });
            });
        }

        return SearchForm;
    }
);
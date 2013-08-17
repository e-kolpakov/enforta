/*global define*/
define(
    ['jquery'],
    function ($) {
        function SearchForm(form_selector, form_prefix) {
            var that = this;
            this.form = $(form_selector);
            this._listeners = [];

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
            };

            this.submit = function () {
                var data = this.get_data();
                for (var i = 0; i < this._listeners.length; i++) {
                    var callback = this._listeners[i];
                    callback(data);
                }
            };
            $(document).ready(function () {
                $("button.search-btn", this.form).click(function (e) {
                    e.preventDefault();
                    that.submit();
                    return false;
                });
                $("button.reset-btn", this.form).click(function (e) {
                    e.preventDefault();
                    that.clear();
                    return this;
                });
            });
        }

        return SearchForm;
    }
);
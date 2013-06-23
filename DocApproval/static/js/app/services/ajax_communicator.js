/*global define*/
define(['jquery', 'libjquery/jquery.cookie'], function ($) {
    function Communicator(csrf_token) {
        var csrf = csrf_token || $.cookie('csrftoken');
        if (csrf) {
            $.ajaxSetup({
                beforeSend: function (xhr) {
                    xhr.setRequestHeader("X-CSRFToken", csrf);
                }
            });
        }

        var default_options = {
            dataType: 'json',
            type: 'POST'
        };

        this.make_request = function (ajax_options, data) {
            var eff_options = $.extend({}, default_options, ajax_options);
            if (data) {
                eff_options.data = data;
            }
            return $.ajax(eff_options).promise();
        };
    }

    return Communicator;
});
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

        this.make_request = function (ajax_options) {
            var eff_options = $.extend({}, default_options, ajax_options);
            return $.ajax(eff_options).promise();
        };
    }

    return Communicator;
});
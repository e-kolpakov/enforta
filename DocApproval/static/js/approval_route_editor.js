(function ($) {
    //TODO: add real logging/notifying
    var logger = console ? console.log : alert;
    var ui_notifier = logger;

    function download_approver_list(target_url) {
        return $.ajax({
            type: 'POST',
            url: target_url,
            dataType: 'json'
        });
    }

    function restore_initial_data(initial_data) {
        logger("Initial Data:");
        logger(initial_data);
    }

    $.fn.approval_route_editor = function (elem, options, initial_data) {
        var approver_list_promise = download_approver_list(options.approvers_source_url);
        approver_list_promise.done(function (data, textStatus, jqXHR) {
            logger("Approvers:")
            logger(data);
            restore_initial_data(initial_data);
        });

        //TODO: add real error handling
        approver_list_promise.fail(function (jqXHR, textStatus, errorThrown) {
            ui_notifier(errorThrown);
        });
        approver_list_promise.resolve();
    };
}(window.jQuery));
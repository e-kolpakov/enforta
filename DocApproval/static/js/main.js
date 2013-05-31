/*global requirejs, require, globals*/

requirejs.config({
    baseUrl: globals.static_root + "js/lib",
    paths: {
        'jquery': 'jquery/jquery',
        'jquery-ui': 'jquery/jquery-ui',
        'bootstrap': 'bootstrap',
        'libjquery': 'jquery',

        'app': "../app",
        'pages': '../pages' //page-specific scripts go here
    },
    shim: {
        "bootstrap": {
            deps: ["jquery"],
            exports: "$.fn.modal"
        }
    }
});


// taken from
// http://stackoverflow.com/questions/11674824/how-to-use-requirejs-build-profile-r-js-in-a-multi-page-project/11730147#11730147
require(['jquery', 'bootstrap', 'app/startup'],
    function ($) {
        // the start module is defined on the same script tag of data-main.
        var startModuleName = $("script[data-main][data-start]").attr("data-start");

        if (startModuleName) {
            require([startModuleName], function (startModule) {
                $(function () {
                    var fn = $.isFunction(startModule) ? startModule : startModule.init;
                    if (fn) {
                        fn();
                    }
                });
            });
        }
    }
);
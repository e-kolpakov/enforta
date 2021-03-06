/*global requirejs, require, globals*/

requirejs.config({
    baseUrl: globals.static_root + "js/lib",
    urlArgs: "version=v0.8.4.10",
    paths: {
        'jquery': 'jquery/jquery',
        'jquery-ui': 'jquery/jquery-ui',
        'bootstrap': 'bootstrap',
        'libjquery': 'jquery',

        'app': "../app",
        'pages': '../pages' //page-specific scripts go here
    },
    shim: {
        'bootstrap': {
            deps: ["jquery"],
            exports: "$.fn.modal"
        },
        'jquery-ui': {
            deps: ["jquery"]
        }
    }
});


// taken from
// http://stackoverflow.com/questions/11674824/how-to-use-requirejs-build-profile-r-js-in-a-multi-page-project/11730147#11730147
require(
    [
        //common libs
        'jquery', 'bootstrap', 'jquery-ui',
        'app/startup', 'app/dispatcher', 'app/widgets/collapsible-panel',
        // behaviors
        'app/behaviors/list_approve', 'app/behaviors/impersonation_list', 'app/behaviors/notifications',
        //ie media queries support
        'ie/respond.min', 'ie/html5shiv'//, 'ie/css3-mediaqueries'
    ],
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
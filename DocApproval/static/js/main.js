/*global requirejs, globals*/

requirejs.config({
    baseUrl: globals.static_root + "js/lib",
    paths: {
        'jquery': 'jquery/jquery',
        'jquery-ui': 'jquery/jquery-ui',
        'bootstrap': 'bootstrap',
        'libjquery': 'jquery',

        'app': "../app",
        'root': "../"
    }
});


requirejs(['jquery', 'bootstrap', 'root/startup'], function ($) {
    $(function () {

    });
});
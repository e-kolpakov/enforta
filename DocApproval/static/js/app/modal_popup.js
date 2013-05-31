/*global define*/
define(
    ['jquery', 'bootstrap'],
    function ($) {
        function ModalPopup(buttons) {

            var popup = make_elem("div").addClass("modal hide fade").attr({
                'role': 'dialog',
                'aria-labelledby': 'popup-label',
                'aria-hidden': 'true'
            });
            var header = make_elem("div").addClass("modal-header").appendTo(popup);
            make_elem("button").addClass("close").text('x')
                .attr({'data-dismiss': 'modal', 'aria-hidden': 'true'})
                .appendTo(header);
            var caption = make_elem("h4").attr("id", 'popup-label').appendTo(header);
            var body = make_elem("div").addClass("modal-body").appendTo(popup);
            var footer = make_elem("div").addClass("modal-footer").appendTo(popup);

            function make_elem(elem) {
                return $("<" + elem + "></" + elem + ">");
            }

            function make_button(btn_type, callback) {
                make_elem("button").addClass('btn').appendTo(footer);
            }

            for (var btn in buttons) {
                if (!buttons.hasOwnProperty(btn)) continue;
                make_button(buttons.btn, function () {
                });
            }

            this.set_header = function (header) {
                caption.empty();
                caption.text(header);
            };

            this.set_content = function (message) {
                body.empty();
                body.text(message);
            };

            this.show = function () {
                popup.modal({
                    backdrop: true,
                    keyboard: true
                });
            };
        }

        return ModalPopup;
    }
);
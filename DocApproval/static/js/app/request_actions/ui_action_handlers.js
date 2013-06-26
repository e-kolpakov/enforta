/*global define*/
define(
    ['extend', 'app/services/ui_interaction_manager', 'app/services/logger', 'app/messages'],
    function (extend, UIManager, Logger, messages) {
        // Always keep in sync with codes in request_management/actions.py
        var ActionCodes = {
            TO_APPROVAL: 'to_approval',
            TO_PROJECT: 'to_project',
            APPROVE: 'approve',
            REJECT: 'reject',
            SET_PAID: 'set_paid'
        };

        var Messages = messages.ActionMessages;

        var ui_manager = new UIManager();

        var logger = new Logger();

        function BaseActionHandler() {
        }

        BaseActionHandler.prototype = {
            validate_callback: function (callback_to_validate) {
                return (callback_to_validate && typeof callback_to_validate === "function");
            },

            process_action: function (callback) {
                logger.log("Should be overridden in child classes");
                callback({post_action: false});
            },

            handle: function (callback) {
                if (this.validate_callback(callback)) {
                    this.process_action(callback);
                }
            }
        };

        function StatusActionHandler(request_pk) {
            this.action_code = "";
            this.request_pk = request_pk;
            this.confrimation_message = "";
        }

        extend(StatusActionHandler, BaseActionHandler);
        StatusActionHandler.prototype.process_action = function (callback) {
            ui_manager.confirmation(this.confrimation_message, function (is_confirmed) {
                callback(this.action_code, this.request_pk, {post_action: is_confirmed});
            }.bind(this));
        };

        var ToApprovalActionHandler = function (request_pk) {
            this.action_code = ActionCodes.TO_APPROVAL;
            this.request_pk = request_pk;
            this.confrimation_message = Messages.confirm_to_negotiation;
        };
        extend(ToApprovalActionHandler, StatusActionHandler);

        var ToProjectActionHandler = function (request_pk) {
            this.action_code = ActionCodes.TO_PROJECT;
            this.request_pk = request_pk;
            this.confrimation_message = Messages.confirm_to_project;
        };
        extend(ToProjectActionHandler, StatusActionHandler);

        var SetPaidActionHandler = function (request_pk) {
            this.action_code = ActionCodes.SET_PAID;
            this.request_pk = request_pk;
        };
        extend(SetPaidActionHandler, StatusActionHandler);
        SetPaidActionHandler.prototype.process_action = function (callback) {
            ui_manager.date_input(Messages.prompt_for_paid_date, function (ui_result) {
                callback(this.action_code, this.request_pk, {
                    post_action: ui_result.success,
                    data: {
                        paid_date: ui_result.paid_date
                    }
                });
            }.bind(this));
        };

        function ApprovalActionHandler(request_pk) {
            this.action_code = "";
            this.request_pk = request_pk;
        }

        extend(ApprovalActionHandler, BaseActionHandler);
        ApprovalActionHandler.prototype.process_action = function (callback) {
            ui_manager.input(Messages.confirm_approve, this.action_code, this.request_pk, function (ui_result) {
                callback(this.action_code, this.request_pk, {
                    post_action: ui_result.success,
                    data: {
                        comment: ui_result.comment,
                        on_behalf_of: ui_result.on_behalf_of
                    }
                });
            }.bind(this));
        };

        var ApproveActionHandler = function (request_pk) {
            this.action_code = ActionCodes.APPROVE;
            this.request_pk = request_pk;
        };

        var RejectActionHandler = function (request_pk) {
            this.action_code = ActionCodes.REJECT;
            this.request_pk = request_pk;
        };


        extend(ApproveActionHandler, ApprovalActionHandler);
        extend(RejectActionHandler, ApprovalActionHandler);

        return {
            ActionCodes: ActionCodes,
            ToApprovalActionHandler: ToApprovalActionHandler,
            ToProjectActionHandler: ToProjectActionHandler,
            ApproveActionHandler: ApproveActionHandler,
            RejectActionHandler: RejectActionHandler,
            SetPaidActionHandler: SetPaidActionHandler
        };
    }
);
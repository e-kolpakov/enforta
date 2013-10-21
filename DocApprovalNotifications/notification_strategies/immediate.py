from DocApproval.models import UserProfile
from DocApprovalNotifications.models import Notification
from DocApprovalNotifications.notification_strategies.base import BaseStrategy, ApproversInStepStrategyMixin, BaseAccountingStrategyMixin

NotificationType = Notification.NotificationType


class NotifyApproversInNextStepStrategy(BaseStrategy, ApproversInStepStrategyMixin):
    def execute(self, event):
        next_approvers = self.get_approvers_in_next_step(event)

        for approver in next_approvers:
            self._create_notification(event, approver, False, NotificationType.APPROVE_REQUIRED)


class NotifyCreatorStrategy(BaseStrategy):
    notification_type = None

    def execute(self, event):
        request = self._get_event_entity(event)
        creator = request.creator
        self._create_notification(event, creator, False, self.notification_type)


class NotifyApproverRequestApprovedStrategy(NotifyCreatorStrategy):
    notification_type = NotificationType.REQUEST_APPROVED


class NotifyApproverRequestRejectedStrategy(NotifyCreatorStrategy):
    notification_type = NotificationType.REQUEST_REJECTED


class NotifyApproverRequestApprovalCompleteStrategy(NotifyCreatorStrategy):
    notification_type = NotificationType.REQUEST_FINAL_APPROVE


class NotifyAllUsersStrategy(BaseStrategy):
    include_creator = True
    notification_type = None

    def execute(self, event):
        request = self._get_event_entity(event)
        recipients = UserProfile.objects.get_active_users()

        for recipient in recipients:
            if self.include_creator or recipient != request.creator:  # creator gets it's own email
                self._create_notification(event=event, notification_recipient=recipient, recurring=False,
                                          notification_type=self.notification_type)


class NotifyAllUsersFinalApproveStrategy(NotifyAllUsersStrategy):
    include_creator = False
    notification_type = NotificationType.REQUEST_FINAL_APPROVE


class NotifyAllUsersContractExpiredStrategy(NotifyAllUsersStrategy):
    include_creator = True
    notification_type = NotificationType.CONTRACT_EXPIRED


class NotifyAccountingStrategy(BaseStrategy, BaseAccountingStrategyMixin):
    def execute(self, event):
        for accountant in self._get_accounting_members():
            self._create_notification(event=event, notification_recipient=accountant, recurring=False,
                                      notification_type=NotificationType.CONTRACT_PAYMENT_REQUIRED)
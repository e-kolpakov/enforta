from DocApprovalNotifications.models import Notification
from DocApprovalNotifications.notification_strategies.base import BaseStrategy, ApproversInStepStrategyMixin, BaseAccountingStrategyMixin

NotificationType = Notification.NotificationType


class RecurringApproversInNextStepStrategy(BaseStrategy, ApproversInStepStrategyMixin):
    def execute(self, event):
        approvers = self.get_approvers_in_next_step(event)

        for approver in approvers:
            self._create_notification(event=event, notification_recipient=approver, recurring=True,
                                      notification_type=NotificationType.APPROVE_REQUIRED_REMINDER)


class RecurringNotificationAccountingStrategy(BaseStrategy, BaseAccountingStrategyMixin):
    def execute(self, event):
        for accountant in self._get_accounting_members():
            self._create_notification(event=event, notification_recipient=accountant, recurring=True,
                                      notification_type=NotificationType.CONTRACT_PAYMENT_REQUIRED_REMINDER)
from DocApprovalNotifications.models import Notification
from DocApprovalNotifications.notification_strategies.base import BaseStrategy, ApproversInStepStrategyMixin


class RecurringApproversInNextStepStrategy(BaseStrategy, ApproversInStepStrategyMixin):
    def execute(self, event):
        approvers = self.get_approvers_in_next_step(event)

        for approver in approvers:
            self._create_notification(
                event=event, notification_recipient=approver, repeating=True,
                notification_type=Notification.NotificationType.APPROVE_REQUIRED_REMINDER)

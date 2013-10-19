from DocApprovalNotifications.models import Event, Notification
from DocApprovalNotifications.notification_strategies.base import BaseStrategy

# REQUEST_APPROVAL_STARTED - immediate: next approver(s)
# REQUEST_APPROVED -    immediate: next approver(s), creator;
# REQUEST_REJECTED -    immediate: creator;
# REQUEST_FINAL_APPROVE - immediate: creator, all users(?)
# CONTRACT_EXPIRED - immediate: all users(?)


class BaseImmediateStrategy(BaseStrategy):
    def _create_notification(self, event, recipient):
        Notification.objects.create(event=event, notification_recipient=recipient, repeating=False)


class NotifyNextApproversStrategy(BaseImmediateStrategy):
    def execute(self, event):
        request = self._get_event_entity(event)
        next_approval_step = event.params.get(Event.ParamKeys.STEP_NUMBER, 0) + 1
        next_approvers = request.approval_route.get_approvers(next_approval_step)

        for approver in next_approvers:
            self._create_notification(event, approver)
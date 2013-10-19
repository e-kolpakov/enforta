from DocApprovalNotifications.models import Event, Notification
from DocApprovalNotifications.notification_strategies.base import BaseStrategy

NotificationType = Notification.NotificationType

# REQUEST_APPROVAL_STARTED - immediate: next approver(s)
# REQUEST_APPROVED -    immediate: next approver(s), creator;
# REQUEST_REJECTED -    immediate: creator;
# REQUEST_FINAL_APPROVE - immediate: creator, all users(?)
# CONTRACT_EXPIRED - immediate: all users(?)


class BaseImmediateStrategy(BaseStrategy):
    def _create_notification(self, event, recipient, notification_type):
        Notification.objects.create(event=event, notification_recipient=recipient,
                                    repeating=False, notification_type=notification_type)


class NotifyApproversInNextStepStrategy(BaseImmediateStrategy):
    def execute(self, event):
        request = self._get_event_entity(event)
        next_approval_step = event.params.get(Event.ParamKeys.STEP_NUMBER, 0) + 1
        next_approvers = request.approval_route.get_approvers(next_approval_step)

        for approver in next_approvers:
            self._create_notification(event, approver, NotificationType.APPROVE_REQUIRED)


class NotifyCreatorStrategy(BaseImmediateStrategy):
    notification_type = None

    def execute(self, event):
        request = self._get_event_entity(event)
        creator = request.creator
        self._create_notification(event, creator, self.notification_type)


class NotifyApproverRequestApprovedStrategy(NotifyCreatorStrategy):
    notification_type = NotificationType.REQUEST_APPROVED


class NotifyApproverRequestRejectedStrategy(NotifyCreatorStrategy):
    notification_type = NotificationType.REQUEST_REJECTED


class NotifyApproverRequestApprovalCompleteStrategy(NotifyCreatorStrategy):
    notification_type = NotificationType.REQUEST_FINAL_APPROVE
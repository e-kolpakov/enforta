from DocApprovalNotifications.models import Notification
from DocApprovalNotifications.notification_strategies.base import BaseStrategy, ApproversInStepStrategyMixin


class BaseCleanStrategy(BaseStrategy):
    def _get_notifications_of_same_entity_for_users(self, event, user_ids, notification_type=None):
        queryset = self._get_notifications_of_same_entity(event).filter(
            notification_recipient__in=user_ids
        )
        if notification_type:
            queryset = queryset.filter(notification_type=notification_type)

        return queryset


class BaseCleanApproversStrategy(BaseCleanStrategy):
    def execute(self, event):
        approver_ids = self.get_approver_ids(event)

        all_requests = self._get_notifications_of_same_entity_for_users(
            event, approver_ids, Notification.NotificationType.APPROVE_REQUIRED
        )
        active_requests = list(all_requests.filter(dismissed=False))

        all_requests.update(dismissed=True)

        for request in active_requests:
            # TODO: a little bug here - upon rejecting notification is still sent to rejector
            # as REQUEST_APPROVAL_CANCELLED event is handled first
            if request.notification_recipient != event.sender:
                self._create_notification(
                    event=event, notification_recipient=request.notification_recipient, repeating=False,
                    notification_type=Notification.NotificationType.APPROVE_NO_LONGER_REQUIRED
                )

    def get_approver_ids(self, event):
        return set()


class CleanAllApproversStrategy(BaseCleanApproversStrategy):
    def get_approver_ids(self, event):
        request = self._get_event_entity(event)
        return set(step.approver.pk for step in request.approval_route.get_all_steps())


class CleanApproversInCurrentStepStrategy(BaseCleanApproversStrategy, ApproversInStepStrategyMixin):
    def get_approver_ids(self, event):
        return set(approver.pk for approver in self.get_approvers_in_current_step(event))
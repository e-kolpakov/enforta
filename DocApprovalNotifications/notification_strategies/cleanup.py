import collections
from DocApprovalNotifications.models import Notification
from DocApprovalNotifications.notification_strategies.base import BaseStrategy, ApproversInStepStrategyMixin

NotificationType = Notification.NotificationType


class BaseCleanStrategy(BaseStrategy):
    def _get_notifications_of_same_entity_for_users(self, event, user_ids, notification_type=None):
        queryset = self._get_notifications_of_same_entity(event).filter(
            notification_recipient__in=user_ids
        )
        if notification_type:
            if isinstance(notification_type, collections.Iterable):
                target_types = notification_type
            else:
                target_types = [notification_type]
            queryset = queryset.filter(notification_type__in=target_types)

        return queryset


class BaseCleanApproversStrategy(BaseCleanStrategy):
    def execute(self, event):
        approver_ids = self.get_approver_ids(event)

        all_requests = self._get_notifications_of_same_entity_for_users(
            event, approver_ids,
            notification_type=(NotificationType.APPROVE_REQUIRED, NotificationType.APPROVE_REQUIRED_REMINDER)
        )
        active_requests = list(all_requests.filter(dismissed=False))

        all_requests.update(dismissed=True)

        no_longer_required_sent = set()

        for request in active_requests:
            recipient = request.notification_recipient
            # TODO: a little bug here - upon rejecting notification is still sent to rejecter
            # as REQUEST_APPROVAL_CANCELLED event is handled first
            if recipient != event.sender and recipient not in no_longer_required_sent:
                no_longer_required_sent.add(recipient)  # prevent double sending
                self._create_notification(
                    event=event, notification_recipient=recipient, repeating=False,
                    notification_type=NotificationType.APPROVE_NO_LONGER_REQUIRED
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
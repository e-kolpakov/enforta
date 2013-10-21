from DocApprovalNotifications.models import Notification
from DocApprovalNotifications.notification_strategies.base import BaseStrategy, ApproversInStepStrategyMixin, BaseAccountingStrategyMixin
from DocApprovalNotifications.utils import as_collection

NotificationType = Notification.NotificationType


class BaseCleanStrategy(BaseStrategy):
    def _get_notifications_of_same_entity_for_users(self, event, user_ids, notification_type=None):
        queryset = self._get_notifications_of_same_entity(event).filter(
            notification_recipient__in=user_ids
        )
        if notification_type:
            queryset = queryset.filter(notification_type__in=as_collection(notification_type))

        return queryset

    def _all_notifications_query(self, event, user_ids, notification_type=None):
        return self._get_notifications_of_same_entity_for_users(event, user_ids, notification_type=notification_type)

    def _active_notifications(self, notifications_query):
        return notifications_query.filter(dismissed=False)


class BaseCleanUsersStrategy(BaseCleanStrategy):
    def execute(self, event):
        approver_ids = self.get_approver_ids(event)

        all_notifications = self._all_notifications_query(event, approver_ids, self.get_notification_types())
        active_notification_recipients = set(
            notification.notification_recipient for notification in all_notifications.filter(dismissed=False)
        )

        for recipient in active_notification_recipients:
            # TODO: a little bug here - upon rejecting notification is still sent to rejecter
            # as REQUEST_APPROVAL_CANCELLED event is handled first
            if recipient != event.sender:
                self._create_notification(event=event, notification_recipient=recipient, recurring=False,
                                          notification_type=self.get_deactivation_notification_type())

        all_notifications.update(dismissed=True)

    def get_approver_ids(self, event):
        return set()

    def get_notification_types(self):
        return set()

    def get_deactivation_notification_type(self):
        return None


class CleanAllApproversStrategy(BaseCleanUsersStrategy):
    def get_approver_ids(self, event):
        request = self._get_event_entity(event)
        return set(step.approver.pk for step in request.approval_route.get_all_steps())

    def get_notification_types(self):
        return NotificationType.APPROVE_REQUIRED, NotificationType.APPROVE_REQUIRED_REMINDER

    def get_deactivation_notification_type(self):
        return NotificationType.APPROVE_NO_LONGER_REQUIRED


class CleanApproversInCurrentStepStrategy(BaseCleanUsersStrategy, ApproversInStepStrategyMixin):
    def get_approver_ids(self, event):
        return set(approver.pk for approver in self.get_approvers_in_current_step(event))

    def get_notification_types(self):
        return NotificationType.APPROVE_REQUIRED, NotificationType.APPROVE_REQUIRED_REMINDER

    def get_deactivation_notification_type(self):
        return NotificationType.APPROVE_NO_LONGER_REQUIRED


class CleanAccountingStrategy(BaseCleanUsersStrategy, BaseAccountingStrategyMixin):
    def get_approver_ids(self, event):
        return set(accountant.pk for accountant in self._get_accounting_members())

    def get_notification_types(self):
        return NotificationType.CONTRACT_PAYMENT_REQUIRED, NotificationType.CONTRACT_PAYMENT_REQUIRED_REMINDER

    def get_deactivation_notification_type(self):
        return NotificationType.CONTRACT_PAID
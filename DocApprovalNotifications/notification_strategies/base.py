from DocApproval.constants import Groups
from DocApproval.models import UserProfile
from DocApprovalNotifications.models import Notification, Event


class BaseStrategy(object):
    def __init__(self):
        self._notifications = []

    def _get_event_entity(self, event):
        return event.get_entity()

    def _get_notifications_of_same_entity(self, event):
        return Notification.objects.filter(
            event__entity=event.entity, event__entity_id=event.entity_id
        )

    def _create_notification(self, event, notification_recipient, recurring, notification_type):
        notification = Notification.objects.create(event=event, notification_recipient=notification_recipient,
                                                   recurring=recurring, notification_type=notification_type)
        self._notifications.append(notification)

    def execute(self, event):
        raise NotImplementedError("Execute called on strategy class")

    @property
    def created_notifications(self):
        return self._notifications


class ApproversInStepStrategyMixin(object):
    def get_approvers_in_step(self, event, step):
        request = self._get_event_entity(event)
        return request.approval_route.get_approvers(step)

    def _get_current_approval_step(self, event):
        return event.params.get(Event.ParamKeys.STEP_NUMBER, 0)

    def get_approvers_in_current_step(self, event):
        return self.get_approvers_in_step(event, self._get_current_approval_step(event))

    def get_approvers_in_next_step(self, event):
        return self.get_approvers_in_step(event, self._get_current_approval_step(event) + 1)


class BaseAccountingStrategyMixin(object):
    def _get_accounting_members(self):
        return UserProfile.objects.get_users_in_group(Groups.ACCOUNTANTS)
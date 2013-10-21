from django.db.models.loading import get_model
from DocApproval.constants import Groups
from DocApproval.models import UserProfile
from DocApprovalNotifications.models import Notification, Event


class BaseStrategy(object):
    def _get_entity_model(self, entity):
        app_label, model_name = entity.split(".")
        return get_model(app_label, model_name, seed_cache=False)

    def _get_entity(self, entity, entity_id):
        model = self._get_entity_model(entity)
        return model.objects.get(pk=entity_id)

    def _get_event_entity(self, event):
        return self._get_entity(event.entity, event.entity_id)

    def _get_notifications_of_same_entity(self, event):
        return Notification.objects.filter(
            event__entity=event.entity, event__entity_id=event.entity_id
        )

    def _create_notification(self, event, notification_recipient, recurring, notification_type):
        Notification.objects.create(event=event, notification_recipient=notification_recipient,
                                    recurring=recurring, notification_type=notification_type)

    def execute(self, event):
        raise NotImplementedError("Execute called on strategy class")


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
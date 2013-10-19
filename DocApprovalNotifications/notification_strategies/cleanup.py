from DocApprovalNotifications.models import Notification
from DocApprovalNotifications.notification_strategies.base import BaseStrategy


class CleanAllApproversStrategy(BaseStrategy):
    def execute(self, event):
        request = self._get_event_entity(event)
        all_steps = request.approval_route.get_all_steps()
        approver_ids = set(step.approver.pk for step in all_steps)

        Notification.objects.filter(event__entity=event.entity, event__entity_id=event.event_type,
                                    notification_recipient__in=approver_ids).update(processed=True)

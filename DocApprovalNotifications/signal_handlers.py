import logging
from DocApprovalNotifications.utils import as_collection

from models import Event
from DocApproval.models import (ApprovalProcessAction, RequestStatus)

logger = logging.getLogger(__name__)

action_type_mapping = {
    ApprovalProcessAction.ACTION_APPROVE: Event.EventType.REQUEST_APPROVED,
    ApprovalProcessAction.ACTION_FINAL_APPROVE: Event.EventType.REQUEST_FINAL_APPROVE,
    ApprovalProcessAction.ACTION_REJECT: Event.EventType.REQUEST_REJECTED
}

status_change_mapping = {
    RequestStatus.PROJECT: Event.EventType.REQUEST_APPROVAL_CANCELLED,
    RequestStatus.NEGOTIATION: Event.EventType.REQUEST_APPROVAL_STARTED,
    RequestStatus.NEGOTIATED_NO_PAYMENT: Event.EventType.CONTRACT_PAYMENT_REQUIRED,
    RequestStatus.ACTIVE: (Event.EventType.CONTRACT_ACTIVATED, Event.EventType.CONTRACT_PAID),
    RequestStatus.EXPIRED: Event.EventType.CONTRACT_EXPIRED
}


def handle_approve_action_signal(sender, **kwargs):
    request, user, on_behalf_of = kwargs['request'], kwargs['user'], kwargs['on_behalf_of']
    action_type, step_number, comment = kwargs['action_type'], kwargs['step_number'], kwargs['comment']
    event_type = action_type_mapping.get(action_type, Event.EventType.UNKNOWN)

    params = {
        Event.ParamKeys.STEP_NUMBER: step_number,
        Event.ParamKeys.COMMENT: comment
    }
    if on_behalf_of != user:
        params[Event.ParamKeys.ON_BEHALF_OF] = on_behalf_of

    Event.objects.create(
        event_type=event_type, sender=user, params=params,
        entity="DocApproval.Request", entity_id=request.id,
    )
    logger.info("Approve action signal of type {action_type} as {event_type} for request {request}".format(
        action_type=action_type, event_type=event_type, request=request))


def handle_request_status_change(sender, **kwargs):
    request, new_status, old_status = kwargs['request'], kwargs['new_status'], kwargs['old_status']
    event_types = status_change_mapping.get(new_status.code, Event.EventType.UNKNOWN)
    for event_type in as_collection(event_types):
        Event.objects.create(
            event_type=event_type,
            entity="DocApproval.Request", entity_id=request.id,
            params={
                Event.ParamKeys.OLD_STATUS_CODE: old_status.code,
                Event.ParamKeys.NEW_STATUS_CODE: new_status.code
            }
        )
        logger.info(
            "Request status change {old_status} => {new_status} signal as {event_type} for request {request}".format(
                old_status=old_status, new_status=new_status, event_type=event_type, request=request)
        )


def handle_event_signal(sender, **kwargs):
    from DocApprovalNotifications.notification_strategies.repository import NotificationStrategiesRepository
    from DocApprovalNotifications.tasks import send_notifications

    repo = NotificationStrategiesRepository.get_instance()
    event = kwargs['event']

    for strategy_cls in repo[event.event_type]:
        strategy = strategy_cls()
        strategy.execute(event)
        created_notifications_ids = [notification.pk for notification in strategy.created_notifications]
        send_notifications.delay(created_notifications_ids)


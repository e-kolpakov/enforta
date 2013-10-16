import logging

from django.dispatch import receiver

from models import Event

from DocApproval.models.approval import approve_action_signal
from DocApproval.models.request import request_status_change
from DocApproval.models import (
    ApprovalProcess, ApprovalProcessAction, Request, RequestStatus, get_approval_signal_params
    )

logger = logging.getLogger(__name__)

action_type_mapping = {
    ApprovalProcessAction.ACTION_APPROVE: Event.EventType.REQUEST_APPROVE,
    ApprovalProcessAction.ACTION_FINAL_APPROVE: Event.EventType.REQUEST_FINAL_APPROVE,
    ApprovalProcessAction.ACTION_REJECT: Event.EventType.REQUEST_REJECTED
}

status_change_mapping = {
    RequestStatus.PROJECT: Event.EventType.REQUEST_APPROVAL_CANCELLED,
    RequestStatus.NEGOTIATION: Event.EventType.REQUEST_APPROVAL_STARTED,
    RequestStatus.NEGOTIATED_NO_PAYMENT: Event.EventType.CONTRACT_PAYMENT_REQUIRED,
    RequestStatus.BILL_REQUIRED: Event.EventType.CONTRACT_PAYMENT_REQUIRED,
    RequestStatus.ACTIVE: Event.EventType.CONTRACT_ACTIVATED,
    RequestStatus.OUTDATED: Event.EventType.CONTRACT_EXPIRED
}


@receiver(approve_action_signal, sender=ApprovalProcess)
def handle_approve_action_signal(sender, **kwargs):
    request, user, on_behalf_of, comment, action_type = get_approval_signal_params(**kwargs)
    event_type = action_type_mapping.get(action_type, Event.EventType.UNKNOWN)

    event = Event.objects.create(event_type=event_type, entity="DocApproval.Request", entity_id=request.id, sender=user)
    logger.info("Approve action signal of type {action_type} as {event_type} for request {request}".format(
        action_type=action_type, event_type=event_type, request=request))
    event.process_notifications()


@receiver(request_status_change, sender=Request)
def handle_request_status_change(sender, **kwargs):
    request, new_status, old_status = kwargs['request'], kwargs['new_status'], kwargs['old_status']
    event_type = status_change_mapping.get(new_status.code, Event.EventType.UNKNOWN)
    event = Event.objects.create(event_type=event_type, entity="DocApproval.Request", entity_id=request.id)
    logger.info(
        "Request status change {old_status} => {new_status} signal as {event_type} for request {request}".format(
            old_status=old_status, new_status=new_status, event_type=event_type, request=request))
    event.process_notifications()


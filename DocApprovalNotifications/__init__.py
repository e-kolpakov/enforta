from django.dispatch import receiver
from DocApproval.models import approve_action_signal, request_status_change, ApprovalProcess, Request
from signal_handlers import handle_approve_action_signal, handle_request_status_change


@receiver(approve_action_signal, sender=ApprovalProcess)
def approve_signal_handler(sender, **kwargs):
    handle_approve_action_signal(sender, **kwargs)


@receiver(request_status_change, sender=Request)
def request_status__signal_handler(sender, **kwargs):
    handle_request_status_change(sender, **kwargs)
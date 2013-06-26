#-*- coding: utf-8 -*import logging
import datetime
import logging

from django.db.models import signals as model_signals
from django.contrib.auth.management import create_superuser
from django.contrib.auth import models as auth_app
from django.dispatch import receiver

import reversion

from DocApproval.request_management.status_management import RequestStatusManager
from DocApproval.messages import RequestHistoryMessages


# Prevent interactive question about wanting a superuser created.  (This
# code has to go in this otherwise empty "models" module so that it gets
# processed by the "syncdb" command during database creation.)
model_signals.post_syncdb.disconnect(
    create_superuser,
    sender=auth_app,
    dispatch_uid="django.contrib.auth.management.create_superuser")

from common import Position, City, ModelConstants, Permissions
from approval import (
    ApprovalRoute, TemplateApprovalRoute, ApprovalRouteStep, ApprovalProcess, ApprovalProcessAction,
    NonTemplateApprovalRouteException, ApprovalRouteExceptionBase,
    approve_action_signal, approval_route_changed_signal
    )
from request import (
    Request, RequestStatus, Contract, RequestHistory,
    request_status_change, request_paid
    )
from user import UserProfile, TemporaryUserImpersonation

reversion.register(Request, follow=["contract"])
reversion.register(Contract)

_logger = logging.getLogger(__name__)


def _get_approval_signal_params(**kwargs):
    return kwargs['request'], kwargs['user'], kwargs['on_behalf_of'], kwargs['comment'], kwargs['action_type']


@receiver(approve_action_signal, sender=ApprovalProcess)
def approve_action_handler(sender, **kwargs):
    request, user, on_behalf_of, comment, action_type = _get_approval_signal_params(**kwargs)
    need_save = True
    _logger.info("Handling {1} on request {0}", request, action_type)
    # need to save approval action in history first
    if on_behalf_of != user:
        comment += "\n" + RequestHistoryMessages.ON_BEHALF_OF.format(on_behalf_of.full_name)
    RequestHistory.create_record(
        request=request, action_type=action_type, user=user, comment=comment
    )
    if action_type == ApprovalProcessAction.ACTION_APPROVE:
        pass # no additional processing required
    elif action_type == ApprovalProcessAction.ACTION_FINAL_APPROVE:
        request.status = RequestStatus.objects.get(code=RequestStatus.NEGOTIATED_NO_PAYMENT)
        request.accepted = datetime.datetime.now()
        request.save()
    elif action_type == ApprovalProcessAction.ACTION_REJECT:
        request.status = RequestStatus.objects.get(code=RequestStatus.PROJECT)
        request.save()

# history handlers
@receiver(approval_route_changed_signal, sender=ApprovalRoute)
def history_approve_route_changed_handler(sender, **kwargs):
    request, user = kwargs['request'], kwargs['user']
    RequestHistory.create_record(request=request, action_type=RequestHistory.ROUTE_CHANGED, user=user)


@receiver(model_signals.post_save, sender=Request)
def history_request_save_handler(sender, **kwargs):
    request = kwargs['instance']
    if request.editable:
        RequestHistory.create_record(request=request, action_type=RequestHistory.EDITED, user=request.last_updater)


@receiver(request_status_change, sender=Request)
def status_update_handler(sender, **kwargs):
    request = kwargs['request']
    old_status = kwargs['old_status']
    new_status = kwargs['new_status']
    RequestStatusManager(request).handle_status_update(old_status, new_status)
    RequestHistory.create_record(
        request=request, action_type=RequestHistory.STATUS_CHANGE, user=request.last_updater,
        params={
            'old_status': old_status.code,
            'new_status': new_status.code
        },
    )


@receiver(request_paid, sender=Contract)
def request_paid_handler(sender, **kwargs):
    request = kwargs['request']
    user = kwargs['user']
    RequestHistory.create_record(request=request, action_type=RequestHistory.PAID_DATE_SET, user=user)
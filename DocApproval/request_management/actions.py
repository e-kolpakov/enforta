#-*- coding: utf-8 -*-
import logging
from collections import Mapping

from django.utils.translation import gettext as _
from django.db import transaction

from DocApproval.models import Permissions, RequestStatus, Contract, UserProfile, CanNotImpersonateUser, request_paid
from DocApproval.utilities.permission_checker import PermissionChecker
from DocApproval.utilities.utility import parse_string_to_datetime

_logger = logging.getLogger(__name__)


class RequestActionBase(object):
    code = None
    reload_ask = False
    reload_require = True

    def __init__(self, label, icon=None, *args, **kwargs):
        self.label = label
        self.icon = icon
        super(RequestActionBase, self).__init__(*args, **kwargs)

    def _check_condition(self, user, request):
        raise NotImplementedError("Should be overridden in child classes")

    def _execute(self, user, request):
        raise NotImplementedError("Should be overridden in child classes")

    def _editable_by_user(self, user, request):
        return PermissionChecker(user).check_permission(instance_permissions=Permissions.Request.CAN_EDIT_REQUEST,
                                                        instance=request)

    def is_available(self, user, request):
        return self._check_condition(user, request)

    @transaction.commit_on_success
    def execute(self, user, request, **kwargs):
        result = self._execute(user, request, **kwargs)
        base_result = {
            'reload_ask': self.reload_ask,
            'reload_require': self.reload_require,
        }
        try:
            response = base_result.update(result)
        except TypeError:
            response = base_result
        return response


class StatusBasedAction(RequestActionBase):
    status_code = None

    def is_available(self, user, request):
        if self.status_code is None:
            raise ValueError(
                "Status should not be None. Use RequestActionBase if action does not depend on request status")
        return request.status.code == self.status_code and super(StatusBasedAction, self).is_available(user, request)


class SendToApprovalAction(StatusBasedAction):
    code = 'to_approval'
    reload_ask = False
    reload_require = True
    status_code = RequestStatus.PROJECT

    def _check_condition(self, user, request):
        return self._editable_by_user(user, request)

    def _execute(self, user, request, **kwargs):
        _logger.info(u"User {0} sent request {1} to negotiation status".format(user, request))
        new_status = RequestStatus.objects.get(code=RequestStatus.NEGOTIATION)
        request.status = new_status
        request.save()


class SendToProjectAction(StatusBasedAction):
    code = 'to_project'
    reload_ask = False
    reload_require = True
    status_code = RequestStatus.NEGOTIATION

    def _check_condition(self, user, request):
        return self._editable_by_user(user, request)

    def _execute(self, user, request, **kwargs):
        _logger.info(u"User {0} sent request {1} to project status".format(user, request))
        new_status = RequestStatus.objects.get(code=RequestStatus.PROJECT)
        request.status = new_status
        request.save()


class SetPaidAction(StatusBasedAction):
    code = 'set_paid'
    reload_ask = False
    reload_require = True
    status_code = RequestStatus.NEGOTIATED_NO_PAYMENT
    DATE_TOKEN = 'paid_date'

    def _check_condition(self, user, request):
        return PermissionChecker(user).check_permission(class_permissions=Permissions.Request.CAN_SET_PAID_DATE)

    def _execute(self, user, request, **kwargs):
        paid_date_raw = kwargs.get(self.DATE_TOKEN, None)
        try:
            paid_date = parse_string_to_datetime(paid_date_raw)
            _logger.info(u"User {0} set paid date {1} on request {2}", user, paid_date, request)
            request.contract.paid_date = paid_date
            request.contract.activation_date = paid_date
            request.contract.save()
            request.status = RequestStatus.objects.get(code=RequestStatus.ACTIVE)
            request.save()
            request_paid.send(Contract, request=request, user=user.profile)
        except AttributeError as e:
            _logger.exception(e)
            raise AttributeError(u"Некорректная дата оплаты")


class ApprovalProcessAction(StatusBasedAction):
    status_code = RequestStatus.NEGOTIATION
    reload_ask = False
    reload_require = True

    COMMENT_TOKEN = 'comment'
    ON_BEHALF_OF_TOKEN = 'on_behalf_of'

    def _parse_parameters(self, **kwargs):
        return kwargs.get(self.COMMENT_TOKEN, None), kwargs.get(self.ON_BEHALF_OF_TOKEN, None)

    def is_available(self, user, request):
        return (
            user.profile.can_approve(request) and
            super(ApprovalProcessAction, self).is_available(user, request))

    def _get_approver_profile(self, user, on_behalf_of=None):
        if on_behalf_of:
            try:
                result = UserProfile.objects.get(pk=on_behalf_of)
                if not user.profile.can_impersonate(result):
                    raise CanNotImpersonateUser(user.profile, result)
            except UserProfile.DoesNotExist as e:
                _logger.exception(e)
                raise
        else:
            result = user.profile
        return result


class ApproveAction(ApprovalProcessAction):
    code = 'approve'

    def _check_condition(self, user, request):
        #all the checks are in parent classes
        return True

    def _execute(self, user, request, **kwargs):
        _logger.info(u"User {0} approved request {1}".format(user, request))
        comment, on_behalf_of = self._parse_parameters(**kwargs)

        process = request.approval_route.get_current_process()
        process.step_approved(user.profile, self._get_approver_profile(user, on_behalf_of), comment)


class RejectAction(ApprovalProcessAction):
    code = 'reject'

    def _check_condition(self, user, request):
        #all the checks are in parent classes
        return True

    def _execute(self, user, request, **kwargs):
        _logger.info(u"User {0} rejected request {1}".format(user, request))
        comment, on_behalf_of = self._parse_parameters(**kwargs)

        process = request.approval_route.get_current_process()
        process.step_rejected(user.profile, self._get_approver_profile(user, on_behalf_of), comment)


class RequestActionRepository(Mapping):
    TO_APPROVAL = SendToApprovalAction.code
    TO_PROJECT = SendToProjectAction.code
    APPROVE = ApproveAction.code
    REJECT = RejectAction.code
    SET_PAID = SetPaidAction.code

    _actions = {
        TO_APPROVAL: SendToApprovalAction(_(u"Отправить на утверждение"), icon="icons/request_status/negotiation.png"),
        TO_PROJECT: SendToProjectAction(_(u"Вернуть в статус проекта"), icon="icons/request_status/project.png"),
        APPROVE: ApproveAction(_(u"Утвердить"), icon="icons/action_types/approve.png"),
        REJECT: RejectAction(_(u"Отклонить"), icon="icons/action_types/reject.png"),
        SET_PAID: SetPaidAction(_(u"Оплачена"), icon="icons/action_types/paid.png")
    }

    __getitem__ = _actions.__getitem__
    __iter__ = _actions.__iter__
    __len__ = _actions.__len__
#-*- coding: utf-8 -*-
import logging

from collections import Mapping

from django.utils.translation import gettext as _

from DocApproval.models.common import Permissions
from DocApproval.models.request import RequestStatus

_logger = logging.getLogger(__name__)


class RequestActionBase(object):
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
        return user.has_perm(Permissions._(Permissions.Request.CAN_EDIT_REQUEST), request)

    def is_available(self, user, request):
        return self._check_condition(user, request)

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


class ApprovalProcessAction(StatusBasedAction):
    status_code = RequestStatus.NEGOTIATION
    reload_ask = True
    reload_require = False

    COMMENT_TOKEN = 'comment'

    def is_available(self, user, request):
        return (
            user.profile in request.get_current_approvers() and
            user.has_perm(Permissions._(Permissions.Request.CAN_APPROVE_REQUESTS)) and
            super(ApprovalProcessAction, self).is_available(user, request))

    def _get_approver_profile(self, user):
        # TODO: add support for temporary approver replacement
        return user


class ApproveAction(ApprovalProcessAction):
    code = 'approve'

    def _check_condition(self, user, request):
        #all the checks are in parent classes
        return True

    def _execute(self, user, request, **kwargs):
        _logger.info(u"User {0} approved request {1}".format(user, request))
        comment = kwargs.get(self.COMMENT_TOKEN, None)

        process = request.approval_route.get_current_process()
        process.step_approved(user.profile, self._get_approver_profile(user).profile, comment)


class RejectAction(ApprovalProcessAction):
    code = 'reject'

    def _check_condition(self, user, request):
        #all the checks are in parent classes
        return True

    def _execute(self, user, request, **kwargs):
        _logger.info(u"User {0} rejected request {1}".format(user, request))
        comment = kwargs.get(self.COMMENT_TOKEN, None)

        process = request.approval_route.get_current_process()
        process.step_rejected(user.profile, self._get_approver_profile(user).profile, comment)


class RequestActionRepository(Mapping):
    TO_APPROVAL = SendToApprovalAction.code
    TO_PROJECT = SendToProjectAction.code
    APPROVE = ApproveAction.code
    REJECT = RejectAction.code

    _actions = {
        TO_APPROVAL: SendToApprovalAction(_(u"Отправить на утверждение"), icon="icons/to_approval.png"),
        TO_PROJECT: SendToProjectAction(_(u"Вернуть в статус проекта"), icon="icons/to_project.png"),
        APPROVE: ApproveAction(_(u"Утвердить"), icon="icons/approve.png"),
        REJECT: RejectAction(_(u"Отклонить"), icon="icons/reject.png")
    }

    __getitem__ = _actions.__getitem__
    __iter__ = _actions.__iter__
    __len__ = _actions.__len__
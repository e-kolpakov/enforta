#-*- coding: utf-8 -*-
from collections import Mapping

from django.utils.translation import gettext as _
from DocApproval.models.approval import ApprovalProcessAction
from DocApproval.models.common import Permissions
from DocApproval.models.request import RequestStatus
from DocApproval.request_management.approval_management import ApprovalManager


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
        result = self._execute(user, request)
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
        new_status = RequestStatus.objects.get(code=RequestStatus.PROJECT)
        request.status = new_status
        request.save()


class ApproveAction(StatusBasedAction):
    code = 'approve'
    reload_ask = False
    reload_require = False
    status_code = RequestStatus.NEGOTIATION

    COMMENT_TOKEN = 'comment'

    def _check_condition(self, user, request):
        return user.profile in request.approval_route.get_current_reviewers()

    def _execute(self, user, request, **kwargs):
        comment = kwargs.get(self.COMMENT_TOKEN, '')
        # TODO: add support for temporary approver replacement
        ApprovalManager(request).process_approval_action(user, ApprovalProcessAction.ACTION_APPROVE, comment=comment)


class RequestActionRepository(Mapping):
    TO_APPROVAL = SendToApprovalAction.code
    TO_PROJECT = SendToProjectAction.code
    APPROVE = ApproveAction.code

    _actions = {
        TO_APPROVAL: SendToApprovalAction(_(u"Отправить на утверждение"), icon="icons/to_approval.png"),
        TO_PROJECT: SendToProjectAction(_(u"Вернуть в статус проекта"), icon="icons/to_project.png"),
        APPROVE: ApproveAction(_(u"Утвердить"), icon="icons/approve.png")
    }

    __getitem__ = _actions.__getitem__
    __iter__ = _actions.__iter__
    __len__ = _actions.__len__
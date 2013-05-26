#-*- coding: utf-8 -*-
from collections import Mapping

from django.utils.translation import gettext as _
from DocApproval.models.common import Permissions
from DocApproval.models.request import RequestStatus


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

    def execute(self, user, request):
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


class SendToApprovalAction(RequestActionBase):
    code = 'to_approval'
    reload_ask = False
    reload_require = True

    def _check_condition(self, user, request):
        return request.status.code == RequestStatus.PROJECT and self._editable_by_user(user, request)

    def _execute(self, user, request):
        negotiation_status = RequestStatus.objects.get(code=RequestStatus.NEGOTIATION)
        request.status = negotiation_status
        request.save()


class SendToProjectAction(RequestActionBase):
    code = 'to_project'
    reload_ask = False
    reload_require = True

    def _check_condition(self, user, request):
        return request.status.code == RequestStatus.NEGOTIATION and self._editable_by_user(user, request)

    def _execute(self, user, request):
        negotiation_status = RequestStatus.objects.get(code=RequestStatus.PROJECT)
        request.status = negotiation_status
        request.save()


class RequestActionRepository(Mapping):
    TO_APPROVAL = SendToApprovalAction.code
    TO_PROJECT = SendToProjectAction.code

    _actions = {
        TO_APPROVAL: SendToApprovalAction(_(u"Отправить на утверждение"), icon="icons/to_approval.png"),
        TO_PROJECT: SendToProjectAction(_(u"Вернуть в статус проекта"), icon="icons/to_project.png")
    }

    __getitem__ = _actions.__getitem__
    __iter__ = _actions.__iter__
    __len__ = _actions.__len__
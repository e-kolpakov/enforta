import logging

from django.dispatch.dispatcher import Signal
from django.db import transaction

from DocApproval.models.approval import ApprovalProcessAction
from DocApproval.models.request import Request

_logger = logging.getLogger(__name__)


class ApprovalActionBase(object):
    action_code = None

    def __init__(self, user, request):
        self._user = user
        self._request = request

    def _persist_data(self, process, comment=None, actor=None):
        current_step = process.current_step_number
        step = self._request.approval_route.steps.get(approver=self._user.profile, step_number=current_step)
        eff_actor = actor if actor else self._user.profile

        ApprovalProcessAction.objects.create(process=process, step=step, action=self.action_code, comment=comment,
                                             actor=eff_actor)

    def _get_current_approval_process(self):
        return self._request.approval_route.processes.get(is_current=True)

    def validate(self, actor=None):
        raise NotImplementedError("Must be overridden in child classes")

    def apply(self, actor=None, comment=None):
        raise NotImplementedError("Must be overridden in child classes")


class ApproveAction(ApprovalActionBase):
    action_code = ApprovalProcessAction.ACTION_APPROVE

    def validate(self, actor=None):
        eff_actor = actor if actor else self._user.profile
        return eff_actor in self._request.approval_route.get_current_reviewers()

    @transaction.commit_on_success
    def apply(self, comment=None, actor=None):
        process = self._get_current_approval_process()
        self._persist_data(process, comment, actor)
        if process.current_step_number != process.route.get_steps_count():
            process.current_step_number += 1
            process.save()
        else:
            final_approve_signal.send(Request, request_pk=self._request.pk, user_pk=self._user.pk)


class RejectAction(ApprovalActionBase):
    action_code = ApprovalProcessAction.ACTION_REJECT

    def validate(self, actor=None):
        pass

    @transaction.commit_on_success
    def apply(self, actor=None, comment=None):
        process = self._get_current_approval_process()
        self._persist_data(process, comment, actor)
        reject_signal.send(Request, request_pk=self._request.pk, user_pk=self._user.pk)


class ApprovalManager(object):
    _actions = {
        ApprovalProcessAction.ACTION_APPROVE: ApproveAction,
        ApprovalProcessAction.ACTION_REJECT: ApproveAction,
    }

    def __init__(self, request):
        self._request = request

    def process_approval_action(self, user, action_code, comment=None, actor=None):
        _logger.info(u"User {0} have taken action {1} on request {2}".format(user, action_code, self._request))
        action_class = self._actions[action_code]
        action = action_class(user, self._request)
        success = action.validate(actor)
        if success:
            success = action.apply(comment, actor)


final_approve_signal = Signal(providing_args=(['request_pk', 'user_pk']))
reject_signal = Signal(providing_args=(['request_pk', 'user_pk']))

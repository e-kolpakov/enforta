import logging

from django.db import transaction
from ..models.approval import ApprovalProcess
from ..models.request import RequestStatus


class RequestStatusTransitionBase(object):
    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(RequestStatusTransitionBase, self).__init__(*args, **kwargs)

    def apply(self):
        raise NotImplementedError("Must be overridden in child classes")


class ProjectToNegotiationTransition(RequestStatusTransitionBase):
    _logger = logging.getLogger(__name__ + ".ProjectToNegotiationTransition")

    @transaction.commit_on_success
    def apply(self):
        self._logger.debug("Applying project => negotiation transition")
        try:
            last_attempt = self.request.approval_route.processes.get(is_current=True)
            last_attempt.is_current = False
            last_attempt.save()
            last_attempt_number = last_attempt.attempt_number
        except ApprovalProcess.DoesNotExist:
            last_attempt_number = 0

        new_attempt = ApprovalProcess.objects.create(
            route=self.request.approval_route,
            attempt_number=last_attempt_number + 1,
            is_current=True
        )
        return new_attempt


class NegotiationToProjectTransition(RequestStatusTransitionBase):
    _logger = logging.getLogger(__name__ + ".NegotiationToProjectTransition")

    def apply(self):
        self._logger.debug("Applying negotiation => project transition")
        try:
            last_attempt = self.request.approval_route.processes.get(is_current=True)
            last_attempt.is_current = False
            last_attempt.save()
        except ApprovalProcess.DoesNotExist:
            pass


class NegotiationToNegotiatedNoPaymentTransition(RequestStatusTransitionBase):
    def apply(self):
        pass


class RequestStatusManager(object):
    _logger = logging.getLogger(__name__ + ".RequestStatusManager")

    _valid_transitions = {
        (RequestStatus.PROJECT, RequestStatus.NEGOTIATION): ProjectToNegotiationTransition,
        (RequestStatus.NEGOTIATION, RequestStatus.PROJECT): NegotiationToProjectTransition,
        (RequestStatus.NEGOTIATION, RequestStatus.NEGOTIATED_NO_PAYMENT): NegotiationToNegotiatedNoPaymentTransition
    }

    def __init__(self, request_instance):
        self._request_instance = request_instance

    def handle_status_update(self, old_status, new_status):
        self._logger.debug(
            u"Handling status change on instance {0} - {1} => {2}".format(self._request_instance, old_status,
                                                                          new_status))

        if (old_status.code, new_status.code) in self._valid_transitions:
            transition_class = self._valid_transitions[(old_status.code, new_status.code)]
            transition = transition_class(self._request_instance)
            transition.apply()
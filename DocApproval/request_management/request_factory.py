from django.db import transaction
from guardian.shortcuts import assign_perm
from DocApproval.models import ApprovalRoute, RequestStatus, Permissions
from DocApproval.utilities.utility import wrap_permission


class RequestFactory(object):
    def __init__(self, request_form, contract_form, user):
        self._req_form = request_form
        self._con_form = contract_form
        self._user = user

    @transaction.commit_on_success
    def persist_request(self, override_status=None):
        new_request = self._req_form.save(commit=False)

        approval_route = ApprovalRoute()
        approval_route.name = ApprovalRoute.REQUEST_ROUTE_NAMING_TEMPLATE.format(new_request.name)
        approval_route.save()
        if override_status:
            new_request.status = RequestStatus.objects.get(pk=override_status)
        new_request.creator = self._user.profile
        new_request.last_updater = self._user.profile

        new_request.contract = self._con_form.save()
        new_request.approval_route = approval_route
        new_request.save()

        assign_perm(wrap_permission(Permissions.Request.CAN_VIEW_REQUEST), self._user, new_request)
        assign_perm(wrap_permission(Permissions.Request.CAN_EDIT_REQUEST), self._user, new_request)
        assign_perm(wrap_permission(Permissions.Request.CAN_EDIT_ROUTE), self._user, new_request)

        return new_request
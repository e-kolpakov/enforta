from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from DocApproval.models import Request

from ..models import ApprovalRoute, ApprovalRouteStep


class EditApprovalRouteView(TemplateView):
    template_name = 'approvals/edit_route.html'

    def get(self, request, *args, **kwargs):
        request_pk = int(kwargs.get('request_pk', 0))
        req = get_object_or_404(Request, pk=request_pk)
        return render(request, self.template_name, {
            'req': req
        })
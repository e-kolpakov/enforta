import json
import re

from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import View, TemplateView
from django.contrib.auth.models import User, Permission
from django.db.models import Q
from django.core import serializers
from django.http import HttpResponse

from ..menu import MenuModifierViewMixin, RequestContextMenuManagerExtension
from ..models import ApprovalRoute, Request, Permissions
from ..messages import ApprovalRouteMessages
from ..url_naming.names import ApprovalRoute as ApprovalRouteUrls
from ..utilities.utility import get_url_base
from ..utilities.datatables import JsonConfigurableDatatablesBaseView


class ApprovalRouteEditHandlerView(TemplateView):
    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, request, *args, **kwargs):
        return super(ApprovalRouteEditHandlerView, self).dispatch(request, *args, **kwargs)

    def _get_common_urls(self):
        return {
            'approver_list_url': ApprovalRouteUrls.APPROVERS_JSON,
            'approval_route_backend': ApprovalRouteUrls.APPROVAL_ROUTE_BACKEND_JSON
        }


class ListApprovalRouteView(TemplateView):
    template_name = 'approvals/list.html'
    model = ApprovalRoute
    context_object_name = 'approval_routes'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            'datatables_data': ApprovalRouteUrls.LIST_JSON,
            'datatables_config': ApprovalRouteUrls.LIST_JSON_CONF,
        })


class EditApprovalRouteView(ApprovalRouteEditHandlerView, MenuModifierViewMixin):
    template_name = 'approvals/edit_route.html'
    extender_class = RequestContextMenuManagerExtension

    def get(self, request, *args, **kwargs):
        pk = int(kwargs.get('pk', 0))
        route = get_object_or_404(ApprovalRoute, pk=pk)
        self._apply_extender(request, route.request)

        return render(request, self.template_name, {
            'caption': route.name if route else ApprovalRouteMessages.NEW_APPROVAL_ROUTE,
            'route': route,
            'approver_list_url': ApprovalRouteUrls.APPROVERS_JSON,
            'approval_route_backend': ApprovalRouteUrls.APPROVAL_ROUTE_BACKEND_JSON
        })


class EditTemplateApprovalRouteView(ApprovalRouteEditHandlerView, MenuModifierViewMixin):
    template_name = 'approvals/edit_route.html'

    @method_decorator(permission_required(Permissions._(Permissions.ApprovalRoute.CAN_MANAGE_TEMPLATES)))
    def dispatch(self, request, *args, **kwargs):
        return super(EditTemplateApprovalRouteView, self).dispatch(request, *args, **kwargs)

    extender_class = RequestContextMenuManagerExtension

    def get(self, request, *args, **kwargs):
        pk = int(kwargs.get('pk', 0))
        try:
            route = ApprovalRoute.objects.get(pk=pk)
        except ApprovalRoute.DoesNotExist:
            route = None

        return render(request, self.template_name, {
            'caption': route.name if route else ApprovalRouteMessages.NEW_TEMPLATE_APPROVAL_ROUTE,
            'route': route,
            'approver_list_url': ApprovalRouteUrls.APPROVERS_JSON,
            'approval_route_backend': ApprovalRouteUrls.APPROVAL_ROUTE_BACKEND_JSON
        })


class TemplateApprovalRouteListJson(JsonConfigurableDatatablesBaseView):
    model = ApprovalRoute
    link_field = 'name'
    display_fields = ('name', 'description')

    def get_links_config(self):
        return {
            'name': {
                'base_url': get_url_base(reverse(ApprovalRouteUrls.UPDATE, kwargs={'pk': 0}))
            },
        }

    @method_decorator(permission_required(Permissions._(Permissions.ApprovalRoute.CAN_MANAGE_TEMPLATES)))
    def dispatch(self, request, *args, **kwargs):
        return super(TemplateApprovalRouteListJson, self).dispatch(request, *args, **kwargs)

    def get_initial_queryset(self):
        return self.model.objects.filter(is_template=True)

    def prepare_single_item(self, item):
        return {
            'pk': item.pk,
            'name': item.name,
            'description': item.description
        }


class ApproversListJson(View):
    def _get_all_approvers(self):
        perm = Permission.objects.get(codename=Permissions.Request.CAN_APPROVE_REQUESTS)
        users = User.objects.filter(Q(groups__permissions=perm) | Q(user_permissions=perm)).distinct()
        users.select_related('profile')
        return (user.profile for user in users)

    def post(self, request, *args, **kwargs):
        data = {
            approver.pk: {
                'name': approver.get_short_name()
            }
            for approver in self._get_all_approvers()}
        return HttpResponse(json.dumps(data), content_type="application/json")


class SaveApprovalRouteView(View):
    def post(self, request, *args, **kwargs):
        data = {
            'success': True,
            'bounce': JsonApprovalRouteAdapter().from_post(request.POST)
        }
        return HttpResponse(json.dumps(data), content_type="application/json")


class JsonApprovalRouteAdapter(object):
    step_elem_re = re.compile(r"^steps\[(\d+)]\[]")

    def __init__(self):
        pass

    def from_post(self, post):
        steps = {}
        for item in post.lists():
            match = self.step_elem_re.match(item[0])
            if match:
                steps[match.group(1)] = item[1]

        result = {
            'pk': post.get('pk', 0),
            'name': post.get('name', ''),
            'desc': post.get('desc', ''),
            'steps': steps
        }
        return result

    def to_json(self, route):
        return route
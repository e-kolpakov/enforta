import json
import re
import logging
from collections import defaultdict

from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import View, TemplateView
from django.contrib.auth.models import User, Permission
from django.db.models import Q
from django.http import HttpResponse

from ..menu import MenuModifierViewMixin, RequestContextMenuManagerExtension
from ..models import ApprovalRoute, Request, Permissions
from ..messages import ApprovalRouteMessages
from ..url_naming.names import ApprovalRoute as ApprovalRouteUrls
from ..utilities.utility import get_url_base
from ..utilities.datatables import JsonConfigurableDatatablesBaseView


_logger = logging.getLogger(__name__)


class ApprovalRouteTemplateAdapter(object):
    def __init__(self, **kwargs):
        self.pk = kwargs.get('pk', 0)
        self.name = kwargs.get('name', '')
        self.description = kwargs.get('description', '')
        self.is_template = kwargs.get('is_template', False)
        self.steps = kwargs.get('steps', defaultdict(list))

    @classmethod
    def create(cls, route):
        route_data = ApprovalRouteTemplateAdapter(
            pk=route.pk, is_template=route.is_template,
            name=route.name, description=route.description)
        route_data.set_steps(route.steps.all())
        return route_data

    def set_steps(self, route_steps):
        self.steps = defaultdict(list)
        for step in route_steps:
            self.steps[step.step_number].append(step.approver.pk)

    def steps_as_json(self):
        return json.dumps(self.steps)


class ApprovalRouteEditHandlerView(TemplateView):
    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, request, *args, **kwargs):
        return super(ApprovalRouteEditHandlerView, self).dispatch(request, *args, **kwargs)

    def _get_template_data(self, route=None, is_template_default=False, new_route_name=None):
        if route:
            route_data = ApprovalRouteTemplateAdapter.create(route)
        else:
            route_data = ApprovalRouteTemplateAdapter(
                pk=0, is_template=is_template_default,
                name='', description='')
        return {
            'caption': route_data.name if route_data.name else new_route_name,
            'route_data': route_data,
            'approver_list_url': ApprovalRouteUrls.APPROVERS_JSON,
            'template_route_list_url': ApprovalRouteUrls.TEMPLATES_JSON,
            'approval_route_backend_url': ApprovalRouteUrls.APPROVAL_ROUTE_BACKEND_JSON
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

        return render(request, self.template_name, self._get_template_data(
            route=route,
            new_route_name=ApprovalRouteMessages.NEW_APPROVAL_ROUTE))


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

        return render(request, self.template_name, self._get_template_data(
            route=route,
            is_template_default=True,
            new_route_name=ApprovalRouteMessages.NEW_TEMPLATE_APPROVAL_ROUTE))


class TemplateApprovalRouteListJson(JsonConfigurableDatatablesBaseView):
    model = ApprovalRoute
    link_field = 'name'
    model_fields = ('name', 'description')
    calculated_fields = {'steps_count': ApprovalRouteMessages.STEPS_COUNT, }
    display_fields = ('name', 'description', 'steps_count')


    def get_links_config(self):
        return {
            'name': {
                'base_url': get_url_base(reverse(ApprovalRouteUrls.TEMPLATE_EDIT, kwargs={'pk': 0}))
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
            'description': item.description,
            'steps_count': item.get_steps_count()
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


class TemplatesListJson(View):
    def _get_all_templates(self):
        templates = ApprovalRoute.objects.filter(is_template=True).select_related('steps')
        return templates

    @method_decorator(permission_required(Permissions._(Permissions.ApprovalRoute.CAN_MANAGE_TEMPLATES)))
    def dispatch(self, request, *args, **kwargs):
        return super(TemplatesListJson, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {
            template.pk: ApprovalRouteTemplateAdapter.create(template).__dict__
            for template in self._get_all_templates()}
        return HttpResponse(json.dumps(data), content_type="application/json")


class SaveApprovalRouteView(View):
    step_elem_re = re.compile(r"^steps\[(\d+)]\[]")

    def _get_steps(self, items):
        steps = dict()
        for item in items:
            match = self.step_elem_re.match(item[0])
            if match:
                steps[match.group(1)] = [int(approver_id) for approver_id in item[1]]

        return steps

    def save_route(self, querydict):
        is_template = querydict.get('is_template', 'false') != 'false'
        default_name = ApprovalRouteMessages.DEFAULT_TEMPLATE_APPROVAL_ROUTE_NAME if is_template else ApprovalRouteMessages.NEW_APPROVAL_ROUTE
        steps = self._get_steps(querydict.lists())
        if not steps:
            raise ValueError("Incorrect steps list")

        route = ApprovalRoute.create_or_update_with_steps(
            pk=querydict.get('pk', None),
            name=querydict.get('name', default_name),
            description=querydict.get('desc', ''),
            is_template=is_template,
            steps=steps
        )

        return route

    def post(self, request, *args, **kwargs):
        try:
            self.save_route(request.POST)
            data = {
                'success': True
            }
        except Exception as e:
            _logger.exception(e.message)
            data = {
                'success': False,
                'errors': [e.message]
            }
        return HttpResponse(json.dumps(data), content_type="application/json")
from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from ..menu import MenuModifierViewMixin, RequestContextMenuManagerExtension
from ..models import ApprovalRoute, Request, Permissions
from ..messages import ApprovalRouteMessages
from ..url_naming.names import ApprovalRoute as ApprovalRouteUrls
from ..utilities.utility import get_url_base
from ..utilities.datatables import JsonConfigurableDatatablesBaseView


class ApprovalRouteEditHandlerView(TemplateView):
    pass


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
            'route': route
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
            'route': route
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
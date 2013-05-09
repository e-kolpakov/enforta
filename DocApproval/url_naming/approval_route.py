from django.conf.urls import patterns, url
from names import ApprovalRoute as approval_names

from ..views import approval_route
from ..utilities.datatables import JsonConfigurableDatatablesBaseView as JCDTV

urlpatterns = patterns(
    '',
    url(r"^approvers.json", approval_route.ApproversListJson.as_view()),
    url(r"^list.json.config", approval_route.TemplateApprovalRouteListJson.as_view(), {JCDTV.CONFIG_MARKER: True},
        name=approval_names.LIST_JSON_CONF),
    url(r"^list.json", approval_route.TemplateApprovalRouteListJson.as_view(), name=approval_names.LIST_JSON),

    url(r"^list/", approval_route.ListApprovalRouteView.as_view(), name=approval_names.LIST),

    url(r"^create/", approval_route.EditApprovalRouteView.as_view(), name=approval_names.CREATE),
    url(r"^details/(?P<pk>\d+)", approval_route.EditApprovalRouteView.as_view(), name=approval_names.UPDATE),

    url(r"^template/", approval_route.EditTemplateApprovalRouteView.as_view(), name=approval_names.TEMPLATE_CREATE),
    url(r"^template/(?P<pk>\d+)", approval_route.EditTemplateApprovalRouteView.as_view(),
        name=approval_names.TEMPLATE_EDIT)
)
from django.conf.urls import patterns, url
from names import ApprovalRoute as approval_names

from ..views import approval_route

urlpatterns = patterns(
    '',
    url(r"^details/(?P<request_pk>\d+)", approval_route.EditApprovalRouteView.as_view(), name=approval_names.REQUEST),
    url(r"^update/(?P<request_pk>\d+)", approval_route.EditApprovalRouteView.as_view(), name=approval_names.UPDATE),
)
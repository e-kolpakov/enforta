from django.conf.urls import patterns, url
from django.views.decorators.csrf import ensure_csrf_cookie

from names import Request as request_names
from ..views import (common, request)
from ..extensions.datatables import JsonConfigurableDatatablesBaseView as JCDBV

urlpatterns = patterns(
    '',
    url(r"^list.json.config", request.RequestListJson.as_view(), {JCDBV.CONFIG_MARKER: True},
        name=request_names.LIST_JSON_CONF),
    url(r"^list.json", request.RequestListJson.as_view(), name=request_names.LIST_JSON),

    url(r"^list", ensure_csrf_cookie(request.ListRequestView.as_view()), name=request_names.LIST),
    url(r"^create", request.CreateRequestView.as_view(), name=request_names.CREATE),
    url(r"^details/(?P<pk>\d+)", request.DetailRequestView.as_view(), name=request_names.DETAILS),
    url(r"^edit/(?P<pk>\d+)", request.UpdateRequestView.as_view(), name=request_names.UPDATE),
    url(r"^my_requests/", common.quicktest, name=request_names.MY_REQUESTS),
    url(r"^my_approvals/", common.quicktest, name=request_names.MY_APPROVALS),

    url(r"^archive/(?P<year>\d{4})/(?P<month>\d{2})", request.archive, name=request_names.ARCHIVE_MONTH),
    url(r"^archive/(?P<year>\d{4})", request.archive, name=request_names.ARCHIVE_YEAR),
    url(r"^archive/", request.archive, name=request_names.ARCHIVE),
)
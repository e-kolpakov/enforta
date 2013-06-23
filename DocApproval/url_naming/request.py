from django.conf.urls import patterns, url
from django.views.decorators.csrf import ensure_csrf_cookie

from names import Request as request_names
from ..views import request, approval_list
from ..utilities.datatables import JsonConfigurableDatatablesBaseView as JCDBV

urlpatterns = patterns(
    '',
    # json backends
    url(r"^list.json.config", request.RequestListJson.as_view(), {JCDBV.CONFIG_MARKER: True},
        name=request_names.LIST_JSON_CONF),
    url(r"^list.json", request.RequestListJson.as_view(), name=request_names.LIST_JSON),
    url(r"^actions.json", request.RequestActionsJson.as_view(), name=request_names.ACTIONS_BACKEND_JSON),

    # single request pages
    url(r"^create", request.CreateRequestView.as_view(), name=request_names.CREATE),
    url(r"^edit/(?P<pk>\d+)", request.UpdateRequestView.as_view(), name=request_names.UPDATE),
    url(r"^details/(?P<pk>\d+)", request.DetailRequestView.as_view(), name=request_names.DETAILS),
    url(r"^request_history/(?P<pk>\d+)", request.RequestHistoryView.as_view(),
        name=request_names.REQUEST_HISTORY),
    url(r"^approval_history/(?P<pk>\d+)", request.RequestHistoryView.as_view(),
        {request.RequestHistoryView.AUTO_FILTER_TOKEN: request.RequestHistoryView.APPROVE_ACTIONS_ONLY},
        name=request_names.APPROVAL_HISTORY),

    url(r"^approval_sheet/(?P<pk>\d+)", approval_list.ApprovalListPrint.as_view(), {'as_html': False},
        name=request_names.APPROVAL_SHEET),

    # active request list pages
    url(r"^list", ensure_csrf_cookie(request.ListRequestView.as_view()), name=request_names.LIST),
    url(r"^my_requests/", ensure_csrf_cookie(request.ListRequestView.as_view()),
        {request.ListRequestView.SHOW_ONLY_PARAM: request.ListRequestView.MY_REQUESTS},
        name=request_names.MY_REQUESTS),
    url(r"^my_approvals/", ensure_csrf_cookie(request.ListRequestView.as_view()),
        {request.ListRequestView.SHOW_ONLY_PARAM: request.ListRequestView.MY_APPROVALS},
        name=request_names.MY_APPROVALS),

    # archive request list pages
    url(r"^archive/(?P<year>\d{4})/(?P<month>\d{2})", request.archive, name=request_names.ARCHIVE_MONTH),
    url(r"^archive/(?P<year>\d{4})", request.archive, name=request_names.ARCHIVE_YEAR),
    url(r"^archive/", request.archive, name=request_names.ARCHIVE),
)
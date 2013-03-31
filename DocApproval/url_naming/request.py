from django.conf.urls import patterns, url
from names import Request as request_names

from ..views import common

urlpatterns = patterns(
    '',
    url(r"^list", common.quicktest, name=request_names.LIST),
    url(r"^create", common.quicktest, name=request_names.CREATE),
    url(r"^my_requests/", common.quicktest, name=request_names.MY_REQUESTS),
    url(r"^my_approvals/", common.quicktest, name=request_names.MY_APPROVALS),
)
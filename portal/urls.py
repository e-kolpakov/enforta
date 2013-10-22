from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    '',
    url("", include("DocApproval.urls")),
    url("^notifications/", include("DocApprovalNotifications.urls"))
)


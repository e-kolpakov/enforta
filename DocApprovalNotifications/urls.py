from django.conf import settings
from django.conf.urls import patterns, url
from DocApprovalNotifications.views import NotificationsJsonView

urlpatterns = patterns(
    '',
    url("^notifications.json", NotificationsJsonView.as_view(), name="notifications"),
)

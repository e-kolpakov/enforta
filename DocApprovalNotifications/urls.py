from django.conf import settings
from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse
from DocApprovalNotifications.views import NotificationsJsonView, TemplateDebugView

urlpatterns = patterns(
    '',
    url("^notifications.json", NotificationsJsonView.as_view(), name="notifications"),
)


def static_urls_processor(request):
    return {'static_urls_notifications': {
        'notifications_backend': reverse('notifications')
    }}


if settings.DEBUG:
    urlpatterns += patterns('',
        url("^debug/(?P<notification_id>\d+)(?:/(?P<template>\w+))?", TemplateDebugView.as_view())
    )
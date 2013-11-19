from django.conf import settings
from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse
from django.template import RequestContext
from DocApprovalNotifications.views import NotificationsJsonView, TemplateDebugView

urlpatterns = patterns(
    '',
    url("^notifications.json", NotificationsJsonView.as_view(), name="notifications"),
)


def static_urls_processor(request):
    return {}


if settings.DEBUG:
    urlpatterns += patterns('',
        url("^debug/(?P<notification_id>\d+)(?:/(?P<template>\w+))?", TemplateDebugView.as_view())
    )
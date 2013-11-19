from django.conf import settings
from django.conf.urls import patterns, url
from DocApprovalNotifications.views import NotificationsJsonView, TemplateDebugView

urlpatterns = patterns(
    '',
    url("^notifications.json", NotificationsJsonView.as_view(), name="notifications"),
)


if settings.DEBUG:
    urlpatterns += patterns('',
        url("^debug/(?P<notification_id>\d+)(?:/(?P<template>\w+))?", TemplateDebugView.as_view())
    )
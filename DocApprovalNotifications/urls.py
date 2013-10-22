from django.conf import settings
from django.conf.urls import patterns, url
from DocApprovalNotifications.views import TemplateDebugView, NotificationsView

urlpatterns = patterns(
    '',
    url("^notifications/(?P<notification_id>\d+)", NotificationsView.as_view()),
)

if settings.DEBUG:
    urlpatterns += patterns('',
                            url("^debug/(?P<notification_id>\d+)(?:/(?P<template>\w+))?", TemplateDebugView.as_view())
    )
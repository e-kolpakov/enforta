import json
import logging
from django.conf import settings
from django.core import serializers
from django.http import HttpResponse
from django.utils.timezone import now
from django.shortcuts import render
from django.views.generic import View
from Utilities.humanization import Humanizer
from DocApprovalNotifications.models import Notification


class BaseNotificationView(View):
    def _get_notification(self, notification_id):
        return Notification.objects.get(pk=notification_id)

    def _get_elapsed_human(self, notification):
        return Humanizer().humanize_timedelta(now() - notification.event.timestamp, Humanizer.DATE_PRECISION_DAY)


class TemplateDebugView(BaseNotificationView):
    def get(self, request, *args, **kwargs):
        template = kwargs['template'] if kwargs['template'] else 'default'
        notification_id = kwargs.get('notification_id')

        notification = self._get_notification(notification_id)
        time_elapsed = self._get_elapsed_human(notification)

        data = {
            'notification': notification,
            'event': notification.event,
            'req': notification.event.get_entity(),
            'time_elapsed': time_elapsed,
            'root_url': settings.ROOT_URL
        }

        return render(request, template + ".html", data)


class NotificationsView(BaseNotificationView):
    _logger = logging.getLogger(__name__)

    def _prepare_for_json(self, notification, time_elapsed):
        return {
            'notification': serializers.serialize('json', [notification]),
            'event': serializers.serialize('json', [notification.event]),
            'req': serializers.serialize('json', [notification.event.get_entity()]),
            'time_elapsed': time_elapsed,
            'root_url': settings.ROOT_URL
        }

    def get(self, request, *args, **kwargs):
        notification_id = kwargs.get('notification_id')
        try:
            notification = self._get_notification(notification_id)
            time_elapsed = self._get_elapsed_human(notification)

            data = self._prepare_for_json(notification, time_elapsed)

            wrapped_data = {
                'success': True,
                'notification_data': data
            }
        except Notification.DoesNotExist as e:
            self._logger.exception(e)
            wrapped_data = {
                'success': False,
                'response': None,
                'errors': [unicode(e)]
            }
        return HttpResponse(json.dumps(wrapped_data), content_type="application/json")
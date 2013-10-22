import json
import logging
from django.http import HttpResponse
from django.utils.timezone import now
from django.shortcuts import render
from django.views.generic import View
from DocApproval.utilities.humanization import Humanizer
from DocApprovalNotifications.models import Notification


class BaseNotificationView(View):
    def _get_notification_data(self, notification_id):
        notification = Notification.objects.get(pk=notification_id)
        elapsed = Humanizer().humanize_timedelta(now() - notification.event.timestamp, Humanizer.DATE_PRECISION_DAY)
        return {
            'notification': notification,
            'event': notification.event,
            'request': notification.event.get_entity(),
            'time_elapsed': elapsed
        }


class TemplateDebugView(BaseNotificationView):
    def get(self, request, *args, **kwargs):
        template = kwargs['template'] if kwargs['template'] else 'default'
        notification_id = kwargs.get('notification_id')

        data = self._get_notification_data(notification_id)

        return render(request, template + ".html", data)


class NotificationsView(BaseNotificationView):
    _logger = logging.getLogger(__name__)

    def get(self, request, *args, **kwargs):
        notification_id = kwargs.get('notification_id')
        try:
            data = self._get_notification_data(notification_id)
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
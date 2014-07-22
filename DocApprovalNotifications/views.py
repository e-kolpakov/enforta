import calendar
import logging
from datetime import datetime

from django.shortcuts import render
from django.views.generic import View
from pytz import utc
from DocApprovalNotifications.utils import notification_representation
from Utilities.JsonViewMixin import JsonViewMixin
from DocApprovalNotifications.models import Notification


class TemplateDebugView(View):
    def get(self, request, *args, **kwargs):
        template = kwargs['template'] if kwargs['template'] else 'html_default'
        notification_id = kwargs.get('notification_id')

        notification = Notification.objects.get(pk=notification_id)

        data = notification_representation(notification)

        return render(request, template + ".html", data)


class NotificationsJsonView(View, JsonViewMixin):
    _logger = logging.getLogger(__name__)
    NOTIFICATIONS_PER_PAGE = 20

    def _get_timestamp(self, request, key):
        raw = request.get(key, None)
        return datetime.utcfromtimestamp(float(raw)) if raw else None

    def _get_data(self, request, timestamp):
        notifications = Notification.objects.get_active_immediate().filter(
            notification_recipient=request.user.profile
        ).select_related('event').order_by('-event__timestamp')
        if timestamp:
            notifications = notifications.filter(event__timestamp__gte=timestamp.replace(tzinfo=utc))
        notifications = notifications[:self.NOTIFICATIONS_PER_PAGE:-1]
        notification_ids = [notification.pk for notification in notifications]
        objects = [notification_representation(notification) for notification in notifications]
        Notification.objects.filter(pk__in=notification_ids).update(shown_in_ui=True)
        return {'notifications': objects}

    def get(self, request, *args, **kwargs):
        timestamp = self._get_timestamp(request.GET, 'timestamp')
        client_utc_now = self._get_timestamp(request.GET, 'client_utc_now')
        if timestamp and client_utc_now:
            server_now = datetime.utcnow()
            compensation = server_now - client_utc_now
            timestamp += compensation
        return self._get_json_response(self._get_data, request, timestamp)
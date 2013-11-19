import logging
from django.shortcuts import render
from django.views.generic import View
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

    def _get_data(self, request):
        notifications = Notification.objects.filter(
            notification_recipient=request.user.profile,
            ui_dismissed=False,
            dismissed=False).select_related('event').order_by('event__timestamp')[:self.NOTIFICATIONS_PER_PAGE]
        objects = [notification_representation(notification) for notification in notifications]
        return {'notifications': objects}

    def get(self, request, *args, **kwargs):
        return self._get_json_response(self._get_data, request)
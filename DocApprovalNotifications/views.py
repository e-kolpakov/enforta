import logging
from django.conf import settings
from django.core import serializers
from django.forms import model_to_dict
from django.utils.timezone import now
from django.views.generic import View
from Utilities.JsonViewMixin import JsonViewMixin
from Utilities.humanization import Humanizer
from DocApprovalNotifications.models import Notification


class BaseNotificationView(View):
    def _get_notification(self, notification_id):
        return Notification.objects.get(pk=notification_id)

    def _get_elapsed_human(self, notification):
        return Humanizer().humanize_timedelta(now() - notification.event.timestamp, Humanizer.DATE_PRECISION_DAY)


class NotificationRepresentation(object):
    def __init__(self, notification):
        self._notification = notification

    def to_dict(self):
        return {
            'notification_id': self._notification.pk,
            'notification_type': self._notification.get_notification_type_display()
        }


class NotificationsJsonView(BaseNotificationView, JsonViewMixin):
    _logger = logging.getLogger(__name__)
    NOTIFICATIONS_PER_PAGE = 20

    def _prepare_for_json(self, notification, time_elapsed):
        return {
            'notification': serializers.serialize('json', [notification]),
            'event': serializers.serialize('json', [notification.event]),
            'req': serializers.serialize('json', [notification.event.get_entity()]),
            'time_elapsed': time_elapsed,
            'root_url': settings.ROOT_URL
        }

    def _get_data(self, request):
        notifications = Notification.objects.filter(
            notification_recipient=request.user.profile,
            ui_dismissed=False,
            dismissed=False).select_related('event').order_by('event__timestamp')[:self.NOTIFICATIONS_PER_PAGE]
        objects = [NotificationRepresentation(notification).to_dict() for notification in notifications]
        return {'notifications': objects}

    def get(self, request, *args, **kwargs):
        return self._get_json_response(self._get_data, request)
        # notification_id = kwargs.get('notification_id')
        # try:
        #     notification = self._get_notification(notification_id)
        #     time_elapsed = self._get_elapsed_human(notification)
        #
        #     data = self._prepare_for_json(notification, time_elapsed)
        #
        #     wrapped_data = {
        #         'success': True,
        #         'notification_data': data
        #     }
        # except Notification.DoesNotExist as e:
        #     self._logger.exception(e)
        #     wrapped_data = {
        #         'success': False,
        #         'response': None,
        #         'errors': [unicode(e)]
        #     }
        # return HttpResponse(json.dumps(wrapped_data), content_type="application/json")
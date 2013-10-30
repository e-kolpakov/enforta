from django.conf import settings
from django.template.loader import render_to_string
from django.utils.timezone import now

from DocApproval.utilities.humanization import Humanizer


class NotificationRender(object):
    def _get_notification_data(self, notification):
        time_elapsed = self._get_elapsed_human(notification)

        return {
            'notification': notification,
            'event': notification.event,
            'req': notification.event.get_entity(),
            'time_elapsed': time_elapsed,
            'root_url': settings.ROOT_URL
        }

    def _get_elapsed_human(self, notification):
        return Humanizer().humanize_timedelta(now() - notification.event.timestamp, Humanizer.DATE_PRECISION_DAY)

    def render(self, notification, template):
        """
        @notification Notification
        Renders notification text for use by notification engines
        """
        raise NotImplementedError("Must be overridden")


class EmailNotificationRender(NotificationRender):
    template_mapping = {}

    def render(self, notification, html_template, text_template):
        """
        @notification Notification - notification to render
        @template str - template filename to render against
        """
        data = self._get_notification_data(notification)
        html_body, text_body = render_to_string(html_template, data), render_to_string(text_template, data)
        subject = notification.get_notification_type_display()

        return subject, html_body, text_body

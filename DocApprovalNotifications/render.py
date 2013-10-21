from django.template.loader import render_to_string


class NotificationRender(object):
    def render(self, notification):
        """
        @notification Notification
        Renders notification text for use by notification engines
        """


class EmailNotificationRender(NotificationRender):
    template_mapping = {}

    def render(self, notification):
        """
        @notification Notification - notification to render
        @template str - template filename to render against
        """
        template = self.template_mapping.get(notification.notification_type, 'default.html')
        body = render_to_string(template, {'notification': notification})
        subject = notification.get_notification_type_display()

        return {'body': body, 'subject': subject}

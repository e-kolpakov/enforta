import smtplib
import logging

from django.conf import settings
from django.core.mail import EmailMultiAlternatives, get_connection
from django.template.loader import render_to_string
from DocApprovalNotifications.utils import notification_representation


logger = logging.getLogger(__name__)


class Mailer(object):
    def __init__(self, connection=None):
        self.connection = connection if connection else get_connection()

    def __enter__(self):
        logger.info("Establishing connection to mail server...")
        self.connection.open()
        logger.info("Connection established")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val:
            if exc_type == smtplib.SMTPException:
                logger.exception("SMTP of type %s exception while emailing notifications\n%s", exc_type, exc_val)
            else:
                logger.exception("Unknown exception while emailing notifications\n%s", exc_val)
        self.connection.close()
        logger.info("Connection closed")
        return True

    def _render(self, notification, html_template, text_template):
        """
        @type notification: Notification
        @template str - template filename to render against
        """
        data = notification_representation(notification)
        html_body, text_body = render_to_string(html_template, data), render_to_string(text_template, data)
        subject = notification.get_notification_type_display()

        return subject, html_body, text_body

    def _get_templates(self, notification):
        if notification.recurring:
            return "html_recurring.html", "plain_text_recurring.txt"
        else:
            return "html_default.html", "plain_text_default.txt"

    def _get_recipient(self, notification):
        if hasattr(settings, 'EMAIL_REDIRECT') and settings.EMAIL_REDIRECT:
            return settings.EMAIL_REDIRECT
        else:
            return notification.notification_recipient.email

    def email(self, notification):
        html_tpl, txt_tpl = self._get_templates(notification)
        subject, html_body, text_body = self._render(notification, html_tpl, txt_tpl)
        recipient = self._get_recipient(notification)

        msg = EmailMultiAlternatives(subject=subject, body=text_body, to=[recipient], connection=self.connection)
        msg.attach_alternative(html_body, "text/html")

        logger.info("Sending notification to %s", recipient)
        msg.send()

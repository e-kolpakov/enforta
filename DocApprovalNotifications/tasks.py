from celery import task
from celery.utils.log import get_task_logger
from django.core.mail import get_connection, EmailMultiAlternatives
from DocApprovalNotifications.models import Notification
from DocApprovalNotifications.render import EmailNotificationRender

logger = get_task_logger(__name__)


@task()
def send_immediate_notifications():
    logger.info("Starting send_immediate_notifications")
    target_notifications = Notification.objects.get_active_immediate()
    logger.debug("Fetched target notifications")

    render = EmailNotificationRender()
    connection = get_connection()

    try:
        logger.info("Establishing connection to mail server...")
        connection.open()
        logger.info("Connection established")
        for notification in target_notifications:
            subject, html_body, text_body = render.render(notification, "html_default.html", "plain_text_default.txt")
            recipient = notification.notification_recipient.email

            msg = EmailMultiAlternatives(subject=subject, body=text_body, to=[recipient], connection=connection)
            msg.attach_alternative(html_body, "text/html")

            logger.info("Sending notification to {0}", recipient)
            msg.send()
            logger.debug("Notification {0} sent", notification)
            notification.dismissed = True
            notification.save()
            logger.debug("Notification {0} marked as processed", notification)
    except Exception as e:
        logger.exception("Exception while sending immediate notifications")
    finally:
        connection.close()
        logger.debug("Connection closed")

from celery import task
from celery.utils.log import get_task_logger
from DocApprovalNotifications.emailing import Mailer
from DocApprovalNotifications.models import Notification

logger = get_task_logger(__name__)


@task()
def send_immediate_notifications():
    logger.info("Starting send_immediate_notifications")
    target_notifications = Notification.objects.get_active_immediate()
    logger.debug("Fetched target notifications")

    with Mailer() as mailer:
        for notification in target_notifications:
            mailer.email(notification)
            logger.debug("Notification %d emailed", notification.pk)
            notification.dismissed = True
            notification.save()
            logger.debug("Notification %d marked as processed", notification.pk)
    logger.info("send_immediate_notifications complete")
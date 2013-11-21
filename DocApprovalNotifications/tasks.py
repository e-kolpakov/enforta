# -*- coding=utf-8 -*-
from functools import wraps
from hashlib import md5

from celery import task
from celery.utils.log import get_task_logger

from django.core.cache import cache
from django.utils.timezone import now

from DocApprovalNotifications.emailing import Mailer
from DocApprovalNotifications.models import Notification

logger = get_task_logger(__name__)

LOCK_EXPIRE = 60 * 5


def unique_task(func):
    """
    Decorator to allow only one instance of task running
    http://docs.celeryproject.org/en/latest/tutorials/task-cookbook.html#ensuring-a-task-is-only-executed-one-at-a-time
    """
    # cache.add fails if if the key already exists
    acquire_lock = lambda lock_id: cache.add(lock_id, 'true', LOCK_EXPIRE)
    # memcache delete is very slow, but we have to use it to take
    # advantage of using add() for atomic locking
    release_lock = lambda lock_id: cache.delete(lock_id)

    def _build_lock_id(func, *args, **kwargs):
        md5builder = md5()
        md5builder.update(func.__name__)
        # http://stackoverflow.com/questions/5292273/hash-unicode-string-in-python
        encoder = lambda s: s.encode('utf-8')
        for arg in args:
            md5builder.update(encoder(str(arg)))
        for key, val in kwargs.items():
            md5builder.update(encoder(u"{key}:{val}".format(key=key, val=val)))
        return md5builder.hexdigest()

    @wraps(func)
    def _exec(*args, **kwargs):
        lock_id = _build_lock_id(func, *args, **kwargs)
        logger.debug(u'Lock id is {0}'.format(lock_id))
        if acquire_lock(lock_id):
            logger.debug(u'Lock id {0} acquired'.format(lock_id))
            try:
                result = func(*args, **kwargs)
            finally:
                release_lock(lock_id)
            return result
        else:
            logger.debug('Task {task_name} is being executed by another worker'.format(task_name=func.__name__))

    return _exec


def immediate_sent_callback(notification):
    notification.email_sent = True
    notification.save()
    logger.debug("Notification %d marked as processed", notification.pk)


def recurring_sent_callback(notification):
    time = now()
    notification.last_sent = time
    notification.save()
    logger.debug("Notification %d most_recent_sent set to %s", notification.pk, time)

@task(ignore_result=True)
def send_notifications(notification_ids):
    logger.info("Starting send_notifications")
    target_notifications = Notification.objects.get_active_immediate().filter(pk__in=notification_ids, email_sent=False)
    logger.debug("Fetched target notifications for ids {0}".format(notification_ids))

    total, success = do_send_notifications(target_notifications, processing_callback=immediate_sent_callback)
    logger.info("Completed send_notifications, got {0} notifications, sent {1}".format(total, success))


@task(ignore_result=True)
def send_repeating_notifications():
    logger.info("Starting send_repeating_notifications")
    target_notifications = Notification.objects.get_recurring_to_send()
    logger.debug("Fetched target notifications")

    total, success = do_send_notifications(target_notifications, processing_callback=recurring_sent_callback)
    logger.info("Completed send_repeating_notifications, got {0} notifications, sent {1}".format(total, success))

@task(ignore_result=True)
def suppress_old_immediate_notifications():
    logger.info("Starting clean_old_immediate_notifications")
    Notification.objects.get_old_immediate().update(dismissed=True)
    logger.info("suppressed old immediate notifications")


@task(ignore_result=True)
def resend_failed_immediate_notifications():
    logger.info("Starting resend_failed_immediate_notifications")
    target_notifications = Notification.objects.get_active_immediate().filter(email_sent=False)
    logger.debug("Fetched failed immediate notifications")

    total, success = do_send_notifications(target_notifications, processing_callback=immediate_sent_callback)
    logger.info("Completed resend_failed_immediate_notifications, got {0} notifications, sent {1}".format(total, success))


def do_send_notifications(target_notifications, processing_callback=None):
    notifications = list(target_notifications)
    total, success = len(notifications), 0
    if total > 0:
        with Mailer() as mailer:
            for notification in notifications:
                mailer.email(notification)
                logger.debug("Notification %d emailed", notification.pk)
                if processing_callback:
                    processing_callback(notification)
                success += 1
    return total, success
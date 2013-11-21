import calendar
import collections
import types
from django.conf import settings
from django.utils.timezone import now
from Utilities.humanization import Humanizer


def as_collection(item):
    if isinstance(item, collections.Iterable) and not isinstance(item, types.StringType):
        return item
    else:
        return [item]


def notification_representation(notification):
    """
    @type notification: Notification
    @rtype: dict
    """
    request = notification.event.get_entity()
    result = {
        'notification_id': notification.pk,
        'notification_type': notification.notification_type,
        'notification_type_name': notification.get_notification_type_display(),
        'notification_shown_in_ui': notification.shown_in_ui,
        'notification_email_sent': notification.email_sent,
        'event_type': notification.event.event_type,
        'event_type_name': notification.event.get_event_type_display(),
        'event_timestamp': calendar.timegm(notification.event.timestamp.timetuple()),
        'request_name': request.name,
        'request_url': settings.ROOT_URL + request.get_absolute_url(),
        'time_elapsed': now() - notification.event.timestamp,
        'time_elapsed_human': Humanizer().humanize_timedelta(now() - notification.event.timestamp)
    }
    if notification.event.sender:
        result['sender_name'] = notification.event.sender.full_name

    return result


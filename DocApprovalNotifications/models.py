# -*- coding=utf-8 -*-
from django.db import models
from django.utils.translation import ugettext as _


class ModelConstants:
    MAX_NAME_LENGTH = 500
    MAX_VARCHAR_LENGTH = 4000
    DEFAULT_VARCHAR_LENGTH = 800
    MAX_CODE_VARCHAR_LENGTH = 50


class Event(models.Model):
    class EventType:
        APPROVAL_REQUIRED = "APPROVAL_REQUIRED"
        REQUEST_APPROVAL_STARTED = "REQUEST_APPROVAL_STARTED"
        REQUEST_APPROVAL_CANCELLED = "REQUEST_APPROVAL_CANCELLED"
        REQUEST_APPROVE = "REQUEST_APPROVE"
        REQUEST_REJECTED = "REQUEST_REJECTED"
        REQUEST_FINAL_APPROVE = "REQUEST_FINAL_APPROVE"
        CONTRACT_PAYMENT_REQUIRED = "CONTRACT_PAYMENT_REQUIRED"
        CONTRACT_PAID = "REQUEST_PAID"
        CONTRACT_ACTIVATED = "CONTRACT_ACTIVATED"
        CONTRACT_EXPIRED = "CONTRACT_EXPIRED"
        UNKNOWN = "UNKNOWN"

    event_type = models.CharField(_(u"Тип события"), max_length=ModelConstants.MAX_CODE_VARCHAR_LENGTH, choices=(
        (EventType.APPROVAL_REQUIRED, _(u"Требуется утверждение")),
        (EventType.REQUEST_APPROVE, _(u"Заявка утверждена")),
        (EventType.REQUEST_FINAL_APPROVE, _(u"Заявка полностью утверждена")),
        (EventType.REQUEST_REJECTED, _(u"Заявка отклонена")),
        (EventType.CONTRACT_PAID, _(u"Договор оплачен")),
        (EventType.CONTRACT_EXPIRED, _(u"Истек срок действия договора")),
    ))
    entity = models.CharField(verbose_name=_(u"Сущность"), null=False, blank=False,
                              max_length=ModelConstants.MAX_CODE_VARCHAR_LENGTH)
    entity_id = models.IntegerField(verbose_name=_(u"Первичный ключ сущности"), null=False, blank=False)
    sender = models.ForeignKey("DocApproval.UserProfile", verbose_name=_(u"Пользователь"), null=True)
    timestamp = models.DateTimeField(verbose_name=_(u"Дата и время"), auto_now_add=True, null=False, blank=False)

    def process_notifications(self):
        pass


class Notification(models.Model):
    UI_SHOW_LIMIT = 5
    event = models.ForeignKey(Event, verbose_name=_(u"Событие"))
    notification_recipient = models.ForeignKey("DocApproval.UserProfile", verbose_name=_(u"Получптель"), null=True)
    repeating = models.BooleanField(verbose_name=_(u"Повторяющееся"))
    processed = models.BooleanField(verbose_name=_(u"Погашено"))
    times_shown_in_ui = models.IntegerField(verbose_name=_(u"Показано в интерфейсе"))


# -*- coding=utf-8 -*-
from django.db.models import get_model
from jsonfield import JSONField

from django.db import models
from django.dispatch.dispatcher import Signal, receiver
from django.utils.translation import ugettext as _
from DocApproval.models import ApprovalProcess, approve_action_signal, request_status_change, Request


class ModelConstants:
    MAX_NAME_LENGTH = 500
    MAX_VARCHAR_LENGTH = 4000
    DEFAULT_VARCHAR_LENGTH = 800
    MAX_CODE_VARCHAR_LENGTH = 50


class Event(models.Model):
    class ParamKeys:
        STEP_NUMBER = 'step_number'
        COMMENT = 'comment'
        ON_BEHALF_OF = 'on_behalf_of'

        OLD_STATUS_CODE = 'old_status'
        NEW_STATUS_CODE = 'new_status'

    class EventType:
        REQUEST_APPROVAL_STARTED = "REQUEST_APPROVAL_STARTED"
        REQUEST_APPROVAL_CANCELLED = "REQUEST_APPROVAL_CANCELLED"
        REQUEST_APPROVED = "REQUEST_APPROVED"
        REQUEST_REJECTED = "REQUEST_REJECTED"
        REQUEST_FINAL_APPROVE = "REQUEST_FINAL_APPROVE"
        CONTRACT_PAYMENT_REQUIRED = "CONTRACT_PAYMENT_REQUIRED"
        CONTRACT_PAID = "REQUEST_PAID"
        CONTRACT_ACTIVATED = "CONTRACT_ACTIVATED"
        CONTRACT_EXPIRED = "CONTRACT_EXPIRED"
        UNKNOWN = "UNKNOWN"

    event_type = models.CharField(_(u"Тип события"), max_length=ModelConstants.MAX_CODE_VARCHAR_LENGTH, choices=(
        (EventType.REQUEST_APPROVAL_STARTED, _(u"Начат процесс утверждения")),
        (EventType.REQUEST_APPROVAL_CANCELLED, _(u"Процесс утверждения отменен")),
        (EventType.REQUEST_APPROVED, _(u"Заявка утверждена")),
        (EventType.REQUEST_REJECTED, _(u"Заявка отклонена")),
        (EventType.REQUEST_FINAL_APPROVE, _(u"Заявка полностью утверждена")),
        (EventType.CONTRACT_PAYMENT_REQUIRED, _(u"Требуется оплата договора")),
        (EventType.CONTRACT_PAID, _(u"Договор оплачен")),
        (EventType.CONTRACT_ACTIVATED, _(u"Договор начал действие")),
        (EventType.CONTRACT_EXPIRED, _(u"Истек срок действия договора")),
    ))
    entity = models.CharField(verbose_name=_(u"Сущность"), null=False, blank=False,
                              max_length=ModelConstants.MAX_CODE_VARCHAR_LENGTH)
    entity_id = models.IntegerField(verbose_name=_(u"Первичный ключ сущности"), null=False, blank=False)
    sender = models.ForeignKey("DocApproval.UserProfile", verbose_name=_(u"Пользователь"), null=True)
    params = JSONField(verbose_name=_(u"Дополнительные параметры"), null=True)
    timestamp = models.DateTimeField(verbose_name=_(u"Дата и время"), auto_now_add=True, null=False, blank=False)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(Event, self).save(force_insert, force_update, using, update_fields)
        event_signal.send(self.__class__, event=self)

    def get_entity(self):
        app_label, model_name = self.entity.split(".")
        model = get_model(app_label, model_name, seed_cache=False)
        return model.objects.get(pk=self.entity_id)


class Notification(models.Model):
    class NotificationType:
        APPROVE_REQUIRED = "APPROVE_REQUIRED"
        APPROVE_NO_LONGER_REQUIRED = "APPROVE_NO_LONGER_REQUIRED"
        REQUEST_APPROVED = "REQUEST_APPROVED"
        REQUEST_REJECTED = "REQUEST_REJECTED"
        REQUEST_FINAL_APPROVE = "REQUEST_FINAL_APPROVE"
        CONTRACT_PAYMENT_REQUIRED = "CONTRACT_PAYMENT_REQUIRED"
        CONTRACT_PAID = "CONTRACT_PAID"
        CONTRACT_EXPIRED = "CONTRACT_EXPIRED"

        APPROVE_REQUIRED_REMINDER = "APPROVE_REQUIRED_REMINDER"
        CONTRACT_PAYMENT_REQUIRED_REMINDER = "CONTRACT_PAYMENT_REQUIRED_REMINDER"

    event = models.ForeignKey(Event, verbose_name=_(u"Событие"))
    notification_recipient = models.ForeignKey("DocApproval.UserProfile", verbose_name=_(u"Получптель"), null=True)
    recurring = models.BooleanField(verbose_name=_(u"Повторяющееся"), default=False)
    dismissed = models.BooleanField(verbose_name=_(u"Погашено"), default=False)
    ui_dismissed = models.BooleanField(verbose_name=_(u"Показано в интерфейсе"), default=False)
    notification_type = models.CharField(
        verbose_name=_(u"Тип оповещения"), max_length=ModelConstants.MAX_CODE_VARCHAR_LENGTH, null=False, choices=(
            (NotificationType.APPROVE_REQUIRED, _(u"Требуется утверждение заявки")),
            (NotificationType.APPROVE_NO_LONGER_REQUIRED, _(u"Утверждение заявки более не требуется")),
            (NotificationType.REQUEST_APPROVED, _(u"Заявка утверждена")),
            (NotificationType.REQUEST_REJECTED, _(u"Заявка отклонена")),
            (NotificationType.REQUEST_FINAL_APPROVE, _(u"Заявка полностью утверждена")),
            (NotificationType.CONTRACT_PAYMENT_REQUIRED, _(u"Требуется оплата")),
            (NotificationType.CONTRACT_PAID, _(u"Договор начал действие")),
            (NotificationType.CONTRACT_EXPIRED, _(u"Истек срок действия договора")),

            (NotificationType.APPROVE_REQUIRED_REMINDER, _(u"Напоминание о необходимости утверждения")),
            (NotificationType.CONTRACT_PAYMENT_REQUIRED_REMINDER, _(u"Напоминание о неоплаченных договорах")),
        ))


event_signal = Signal(providing_args=["event"])

from DocApprovalNotifications.signal_handlers import (
    handle_approve_action_signal, handle_request_status_change, handle_event_signal
    )


@receiver(approve_action_signal, sender=ApprovalProcess)
def approve_signal_handler(sender, **kwargs):
    handle_approve_action_signal(sender, **kwargs)


@receiver(request_status_change, sender=Request)
def request_status__signal_handler(sender, **kwargs):
    handle_request_status_change(sender, **kwargs)


@receiver(event_signal, sender=Event)
def event_signal_handler(sender, **kwargs):
    handle_event_signal(sender, **kwargs)

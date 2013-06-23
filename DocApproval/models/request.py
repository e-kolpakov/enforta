#-*- coding: utf-8 -*-
import os
import logging
import datetime

from django.db import models, transaction
from django.dispatch.dispatcher import Signal
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from jsonfield import JSONField
from DocApproval.models.approval import ApprovalProcessAction
from DocApproval.utilities.permission_checker import get_objects_for_users

from .user import UserProfile
from .common import City, ModelConstants, Permissions
from .approval import ApprovalRoute
from DocApproval.url_naming.names import Request as RequestUrls
from DocApproval.utilities.humanization import Humanizer
from DocApproval.constants import Periods


_logger = logging.getLogger(__name__)


class RequestStatus(models.Model):
    PROJECT = "project"
    NEGOTIATION = "negotiation"
    NEGOTIATED_NO_PAYMENT = "negotiated_no_payment"
    ACTIVE = "active"
    OUTDATED = "outdated"
    BILL_REQUIRED = "bill_required"

    code = models.CharField(_(u'Код'), max_length=ModelConstants.MAX_CODE_VARCHAR_LENGTH, primary_key=True,
                            editable=False)
    name = models.CharField(_(u'Статус'), max_length=ModelConstants.DEFAULT_VARCHAR_LENGTH)

    class Meta:
        app_label = "DocApproval"
        verbose_name = _(u'Статус заявки')
        verbose_name_plural = _(u'Статусы заявок')

    def __unicode__(self):
        return self.name


class Contract(models.Model):
    @classmethod
    def _get_path(cls, subpath, filename):
        now = datetime.datetime.now()
        fname, ext = os.path.splitext(filename)
        server_filename = u"{0}({1}){2}".format(fname, now.strftime("%Y_%m_%d_%H_%M_%S"), ext)

        return os.path.join('documents', subpath, now.strftime("%Y_%m_%d"), server_filename)

    def upload_to(self, filename):
        return self._get_path('new', filename)

    def upload_to_signed(self, filename):
        return self._get_path('signed', filename)

    date = models.DateField(_(u'Дата договора'))
    paid_date = models.DateField(_(u'Дата оплаты'), blank=True, null=True)
    activation_date = models.DateField(_(u"Начало действия договора"), blank=True, null=True)
    prolongation = models.BooleanField(_(u'Возможность пролонгации'), blank=True, default=False)

    active_period = models.IntegerField(_(u'Срок действия'))
    active_period_unit = models.CharField(
        verbose_name=_(u'ед. изм.'), null=False, blank=False, default=Periods.DAYS,
        max_length=ModelConstants.MAX_CODE_VARCHAR_LENGTH,
        choices=(
            (Periods.DAYS, _(u"дней")),
            (Periods.WEEKS, _(u"недель")),
            (Periods.MONTHS, _(u"месяцев")),
            (Periods.YEARS, _(u"лет")),
        )
    )

    document = models.FileField(_(u'Документ'), upload_to=upload_to)
    document_signed = models.FileField(_(u'Подписанный документ'), upload_to=upload_to_signed, null=True, blank=True)

    def __unicode__(self):
        return u"{0} {2} {1} {3}".format(_(u"Документ №"), _(u"от"), self.pk, self.date)

    class Meta:
        app_label = "DocApproval"
        verbose_name = _(u"Документ")
        verbose_name_plural = _(u"Документы")

    def active_period_humanize(self):
        return Humanizer().humanize_period(self.active_period, unit=self.active_period_unit)


class RequestManager(models.Manager):
    target_permissions = (
        Permissions.Request.CAN_VIEW_REQUEST,
        Permissions.Request.CAN_VIEW_ALL_REQUESTS
    )

    def get_accessible_requests(self, user):
        return get_objects_for_users(user.profile.effective_accounts, self.target_permissions, klass=Request,
                                     any_perm=True)

    def get_awaiting_approval(self, user):
        return self.get_accessible_requests(user).filter(
            approval_route__steps__approver__in=user.profile.effective_profiles,
            status__code=RequestStatus.NEGOTIATION).distinct()


class Request(models.Model):
    objects = RequestManager()
    name = models.CharField(_(u'Наименование'), max_length=ModelConstants.MAX_NAME_LENGTH)

    city = models.ForeignKey(City, verbose_name=_(u'Город действия'))
    status = models.ForeignKey(RequestStatus, verbose_name=_(u'Статус'))
    contract = models.OneToOneField(Contract, verbose_name=_(u'Документ'), related_name='request')

    creator = models.ForeignKey(UserProfile, verbose_name=_(u'Инициатор'), related_name='requests')
    last_updater = models.ForeignKey(UserProfile, verbose_name=_(u'Последние изменения'),
                                     related_name='requests_last_updated_by')
    send_on_approval = models.ForeignKey(UserProfile, verbose_name=_(u'Отправить на подпись'),
                                         related_name='requests_to_be_sent_on_approval')

    approval_route = models.OneToOneField(ApprovalRoute, verbose_name=_(u"Маршрут утверждения"), null=True)

    created = models.DateField(_(u'Дата создания заявки'), auto_now_add=True)
    updated = models.DateField(_(u'Дата последних изменений'), auto_now=True)
    accepted = models.DateField(_(u'Дата согласования'), blank=True, null=True)

    comments = models.CharField(_(u'Комментарии'), max_length=ModelConstants.MAX_VARCHAR_LENGTH, null=True,
                                blank=True)

    class Meta:
        app_label = "DocApproval"
        verbose_name = _(u'Заявка')
        verbose_name_plural = _(u'Заявки')
        permissions = (
            (Permissions.Request.CAN_CREATE_REQUESTS, _(u"Может создавать запросы на утверждение")),
            (Permissions.Request.CAN_APPROVE_REQUESTS, _(u"Может утверждать документы")),
            (Permissions.Request.CAN_VIEW_ALL_REQUESTS, _(u"Может просматривать любые заявки")),

            (Permissions.Request.CAN_VIEW_REQUEST, _(u"Имеет доступ к данной заявке")),
            (Permissions.Request.CAN_EDIT_REQUEST, _(u"Может редактировать заявку")),
            (Permissions.Request.CAN_EDIT_ROUTE, _(u"Может изменять маршрут утверждения")),

            (Permissions.Request.CAN_SET_PAID_DATE, _(u"Может устанавливать дату оплаты"))
        )

    @transaction.commit_on_success
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        try:
            old_request = Request.objects.get(pk=self.pk)
        except Request.DoesNotExist:
            old_request = None
        super(Request, self).save(force_insert=force_insert, force_update=force_update, using=using,
                                  update_fields=update_fields)
        if old_request and old_request.status != self.status:
            request_status_change.send(Request, request=self, old_status=old_request.status, new_status=self.status)

    def get_absolute_url(self):
        return reverse(RequestUrls.DETAILS, kwargs={'pk': self.pk})

    def __unicode__(self):
        return u"{0} {2} {1} {3}".format(_(u"Заявка"), _(u"от"), self.name, self.created)

    def get_current_approvers(self):
        if self.status.code == RequestStatus.NEGOTIATION:
            return self.approval_route.get_current_approvers()
        else:
            return []

    def is_approved(self):
        return self.status.code in (
            RequestStatus.NEGOTIATED_NO_PAYMENT, RequestStatus.ACTIVE, RequestStatus.BILL_REQUIRED,
            RequestStatus.OUTDATED)

    @property
    def successful_approval(self):
        if not self.is_approved():
            return None

        return self.approval_route.get_successful_process()

    @property
    def route_editable(self):
        return self.editable

    @property
    def editable(self):
        return self.status.code == RequestStatus.PROJECT


class RequestHistory(models.Model):
    EDITED = 'edited'
    STATUS_CHANGE = 'status_change'
    PAID_DATE_SET = 'set_paid'
    ROUTE_CHANGED = 'route_changed'
    APPROVAL = ApprovalProcessAction.ACTION_APPROVE
    REJECTION = ApprovalProcessAction.ACTION_REJECT
    FINAL_APPROVE = ApprovalProcessAction.ACTION_FINAL_APPROVE

    approval_actions = (APPROVAL, REJECTION, FINAL_APPROVE)

    _default_action = "action_types/unknown.png"

    _status_icons = {
        RequestStatus.PROJECT: "request_status/project.png",
        RequestStatus.NEGOTIATION: "request_status/negotiation.png",
        RequestStatus.NEGOTIATED_NO_PAYMENT: "request_status/negotiated_no_payment.png",
        RequestStatus.BILL_REQUIRED: "request_status/bill_required.png",
        RequestStatus.ACTIVE: "request_status/active.png",
        RequestStatus.OUTDATED: "request_status/outdated.png",
    }

    _action_type_icons = {
        EDITED: "action_types/edited.png",
        STATUS_CHANGE: "", # handled differently
        PAID_DATE_SET: "action_types/paid.png",
        ROUTE_CHANGED: "action_types/route_changed.png",
        APPROVAL: "action_types/approve.png",
        REJECTION: "action_types/reject.png",
        FINAL_APPROVE: "action_types/final_approve.png",
    }

    request = models.ForeignKey(Request, verbose_name=_(u"Заявка"), related_name='history')
    action_type = models.CharField(
        max_length=ModelConstants.MAX_CODE_VARCHAR_LENGTH,
        verbose_name=_(u"Тип изменения"),
        choices=(
            (EDITED, _(u"Изменена/создана")),
            (STATUS_CHANGE, _(u"Изменение статуса")),
            (ROUTE_CHANGED, _(u"Изменен маршрут")),
            (APPROVAL, _(u"Утверждена")),
            (REJECTION, _(u"Отклонена")),
            (FINAL_APPROVE, _(u"Полностью утверждена")),
            (PAID_DATE_SET, _(u"Оплачена"))
        )
    )
    actor = models.ForeignKey(UserProfile, verbose_name=_(u"Пользователь"))
    action_date = models.DateTimeField(verbose_name=_(u"Дата и время"), auto_now_add=True)
    action_parameters = JSONField(verbose_name=_(u"Параметры"), null=True)
    comments = models.CharField(max_length=ModelConstants.MAX_VARCHAR_LENGTH,
                                verbose_name=_(u"Дополнительная информация"), null=True)

    @classmethod
    def create_record(cls, request, action_type, user, comment=None, params=None):
        cls.objects.create(request=request, action_type=action_type, actor=user, action_parameters=params,
                           comments=comment)

    class Meta:
        app_label = "DocApproval"
        verbose_name = _(u'Запись об истории заявки')
        verbose_name_plural = _(u'Записи об истории заявки')

    @property
    def icon(self):
        if self.action_type == self.STATUS_CHANGE:
            new_status = self.action_parameters['new_status']
            return self._status_icons.get(new_status, "")
        else:
            return self._action_type_icons.get(self.action_type, "")

    def _get_FIELD_display(self, field):
        if field.name == 'action_type' and self.action_type == self.STATUS_CHANGE:
            status = self.action_parameters.get('new_status')
            result = u"{0}: {1}".format(_(u"Переведена в статус"), RequestStatus.objects.get(pk=status).name)
        else:
            result = super(RequestHistory, self)._get_FIELD_display(field)
        return result

    def __unicode__(self):
        return _(u"[{0}] Заявка {1}: {2}").format(self.action_date, self.request, self.get_action_type_display())


request_status_change = Signal(providing_args=(['request', 'old_status', 'new_status']))
request_paid = Signal(providing_args=(['request']))
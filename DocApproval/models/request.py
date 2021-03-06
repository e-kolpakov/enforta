#-*- coding: utf-8 -*-
import os
import logging
import datetime

from django.db import models, transaction
from django.dispatch.dispatcher import Signal
from django.core.validators import MinValueValidator
from django.core.urlresolvers import reverse
from django.utils.timezone import now
from django.utils.translation import ugettext as _
from guardian.shortcuts import get_objects_for_user, get_users_with_perms

from jsonfield import JSONField

from .user import UserProfile
from .common import City, ModelConstants, Permissions, Currency
from .approval import ApprovalRoute, ApprovalProcessAction

from DocApproval.constants import Periods

from DocApproval.url_naming.names import Request as RequestUrls
from Utilities.humanization import Humanizer
from DocApproval.utilities.permission_checker import PermissionChecker
from DocApproval.utilities.file_upload import ContentTypeRestrictedFileField


_logger = logging.getLogger(__name__)

class RequestStatusManager(models.Manager):
    _cache = {}

    def get_status(self, code):
        if code not in self._cache:
            self._cache[code] = self.get(pk=code)
        return self._cache[code]


class RequestStatus(models.Model):
    PROJECT = "project"
    NEGOTIATION = "negotiation"
    NEGOTIATED_NO_PAYMENT = "negotiated_no_payment"
    ACTIVE = "active"
    EXPIRED = "expired"

    objects = RequestStatusManager()

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
    cost = models.DecimalField(_(u"Стоимость"), max_digits=15, decimal_places=4, validators=[MinValueValidator(0)])
    currency = models.ForeignKey(Currency, verbose_name=_(u'Валюта'), null=False)
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

    document = ContentTypeRestrictedFileField(_(u'Документ'), upload_to=upload_to)
    document_signed = ContentTypeRestrictedFileField(_(u'Подписанный документ'), upload_to=upload_to_signed, null=True,
                                                     blank=True)

    @property
    def expiration_date(self):
        timedelta_params = {self.active_period_unit: self.active_period}
        return self.activation_date + datetime.timedelta(**timedelta_params)

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
        checker = PermissionChecker(user)
        if checker.check_permission(class_permissions=Permissions.Request.CAN_VIEW_ALL_REQUESTS):
            result_qs = self.all()
        else:
            result_qs = get_objects_for_user(user, self.target_permissions, klass=Request, any_perm=True)
            for account in user.profile.effective_accounts:
                result_qs = result_qs | get_objects_for_user(account, self.target_permissions, klass=Request,
                                                             any_perm=True)

        return result_qs

    def get_awaiting_approval(self, user):
        return self.get_accessible_requests(user).filter(
            approval_route__steps__approver__in=user.profile.effective_profiles,
            status__code=RequestStatus.NEGOTIATION).distinct()

    def get_archived_for_year(self, year):
        return self.filter(status__code=RequestStatus.EXPIRED, created__year=year)

    def get_expired_requests(self):
        """
        Returns a queryset of expired requests in active status
        @return: QuerySet[Request]
        """

        # Can't refer to Contract.expiration_date property as it's now in sql
        # Can't make expiration_date a calculated field, as Django does not support calculated fields yet.
        # Solution - extra with manual sql manipulation. Will work with PostgreSQL only
        wrap = lambda name: '"{0}"'.format(name)
        request_table, contract_table = wrap(Request._meta.db_table), wrap(Contract._meta.db_table)
        exp_tpl = "{0}.activation_date + ({0}.active_period::varchar || ' ' || {0}.active_period_unit)::interval <= %s"
        join_tpl = "{req_tbl}.contract_id = {con_tbl}.id"
        return self.filter(status__code=RequestStatus.ACTIVE).extra(
            tables=[contract_table],
            where=[exp_tpl.format(contract_table), join_tpl.format(req_tbl=request_table, con_tbl=contract_table)],
            params=[str(now())]
        )


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

    created = models.DateField(_(u'Создана'), auto_now_add=True)
    updated = models.DateField(_(u'Изменена'), auto_now=True)
    accepted = models.DateField(_(u'Согласована'), blank=True, null=True)
    expired = models.DateField(_(u'Истек срок действия'), blank=True, null=True)

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
        return u"{1} {0} {2}".format(_(u"от"), self.name, self.created)

    def get_current_approvers(self):
        if self.status.code == RequestStatus.NEGOTIATION:
            return self.approval_route.get_current_approvers()
        else:
            return []

    def is_approved(self):
        return self.status.code in (
            RequestStatus.NEGOTIATED_NO_PAYMENT, RequestStatus.ACTIVE,
            RequestStatus.EXPIRED)

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

    @property
    def show_process(self):
        return self.status.code == RequestStatus.NEGOTIATION

    def get_related_users(self):
        return get_users_with_perms(self).select_related('profile')

    def set_expired(self):
        self.expired = now()
        self.status = RequestStatus.objects.get_status(RequestStatus.EXPIRED)
        self.save()


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
        RequestStatus.ACTIVE: "request_status/active.png",
        RequestStatus.EXPIRED: "request_status/outdated.png",
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
            new_status = self.action_parameters.get('new_status')
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
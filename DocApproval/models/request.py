#-*- coding: utf-8 -*-
import os
import datetime

from django.core.urlresolvers import reverse
from django.db import models, transaction
from django.utils.translation import ugettext as _
from guardian.shortcuts import assign_perm, get_objects_for_user

from .user import UserProfile
from .common import City, ModelConstants, Permissions
from .approval import ApprovalRoute
from DocApproval.url_naming.names import Request as RequestUrls
from DocApproval.utilities.humanization import Humanizer


class RequestStatus(models.Model):
    PROJECT = "project"
    NEGOTIATION = "negotiation"
    NEGOTIATED_NO_PAYMENT = "negotiated_no_payment"
    ACTIVE = "active"
    OUTDATED = "outdated"
    BILL_REQUIRED = "bill_required"

    code = models.CharField(_(u'Код'), max_length=ModelConstants.MAX_CODE_VARCHAR_LENGTH, primary_key=True,
                            editable=False)
    status_name = models.CharField(_(u'Статус'), max_length=ModelConstants.DEFAULT_VARCHAR_LENGTH)

    class Meta:
        app_label = "DocApproval"
        verbose_name = _(u'Статус заявки')
        verbose_name_plural = _(u'Статусы заявок')

    def __unicode__(self):
        return self.status_name


class Contract(models.Model):
    @classmethod
    def _get_path(cls, subpath, filename):
        now = datetime.datetime.now()
        cur_date = now.date()
        cur_time = now.time()
        parts = ('documents', subpath, cur_date.strftime("%Y_%m_%d"), cur_time.strftime("%H_%M_%S") + "_" + filename)
        return os.path.join(*parts)

    def upload_to(self, filename):
        return self._get_path('new', filename)

    def upload_to_signed(self, filename):
        return self._get_path('signed', filename)

    date = models.DateField(_(u'Дата договора'))
    active_period = models.IntegerField(_(u'Срок действия'))
    paid_date = models.DateField(_(u'Дата оплаты'), blank=True, null=True)
    activation_date = models.DateField(_(u"Начало действия договора"), blank=True, null=True)
    prolongation = models.BooleanField(_(u'Возможность пролонгации'), blank=True, default=False)

    document = models.FileField(_(u'Документ'), upload_to=upload_to)
    document_signed = models.FileField(_(u'Подписанный документ'), upload_to=upload_to_signed, null=True, blank=True)

    def __unicode__(self):
        return u"{0} {2} {1} {3}".format(_(u"Документ №"), _(u"от"), self.pk, self.date)

    class Meta:
        app_label = "DocApproval"
        verbose_name = _(u"Документ")
        verbose_name_plural = _(u"Документы")

    def active_period_humanize(self):
        return Humanizer().humanize_days(self.active_period)


class RequestManager(models.Manager):
    target_permissions = (
        Permissions.Request.CAN_VIEW_REQUEST,
        Permissions.Request.CAN_VIEW_ALL_REQUESTS
    )

    def get_accessible_requests(self, user):
        return get_objects_for_user(user, self.target_permissions, klass=Request, any_perm=True)

    def get_awaiting_approval(self, user):
        return self.get_accessible_requests(user).filter(approval_route__steps__approver=user,
                                                         status__code=RequestStatus.NEGOTIATION)


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
            (Permissions.Request.CAN_EDIT_ROUTE, _(u"Может изменять маршрут утверждения"))
        )

    def get_absolute_url(self):
        return reverse(RequestUrls.DETAILS, kwargs={'pk': self.pk})

    def __unicode__(self):
        return u"{0} {2} {1} {3}".format(_(u"Заявка"), _(u"от"), self.name, self.created)

    def get_initiator(self):
        return self.creator

    def get_approvers(self):
        return (step.approver for step in self.approval_route.steps)


class RequestFactory(object):
    def __init__(self, request_form, contract_form, user):
        self._req_form = request_form
        self._con_form = contract_form
        self._user = user

    @transaction.commit_on_success
    def persist_request(self, override_status=None):
        new_request = self._req_form.save(commit=False)

        approval_route = ApprovalRoute()
        approval_route.name = ApprovalRoute.REQUEST_ROUTE_NAMING_TEMPLATE.format(new_request.name)
        approval_route.save()
        if override_status:
            new_request.status = RequestStatus.objects.get(pk=override_status)
        new_request.creator = self._user.profile
        new_request.last_updater = self._user.profile

        new_request.contract = self._con_form.save()
        new_request.approval_route = approval_route
        new_request.save()

        assign_perm(Permissions._(Permissions.Request.CAN_VIEW_REQUEST), self._user, new_request)
        assign_perm(Permissions._(Permissions.Request.CAN_EDIT_REQUEST), self._user, new_request)
        assign_perm(Permissions._(Permissions.Request.CAN_EDIT_ROUTE), self._user, new_request)

        return new_request

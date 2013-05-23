#-*- coding: utf-8 -*-
import os
import datetime

from django.db import models, transaction
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.db.models import signals
from django.contrib.auth.management import create_superuser
from django.contrib.auth import models as auth_app
from guardian.shortcuts import assign_perm, remove_perm, get_objects_for_user

from url_naming.names import (Profile as ProfileUrls, Request as RequestUrls)
from DocApproval.utilities.humanization import Humanizer

# Prevent interactive question about wanting a superuser created.  (This
# code has to go in this otherwise empty "models" module so that it gets
# processed by the "syncdb" command during database creation.)

signals.post_syncdb.disconnect(
    create_superuser,
    sender=auth_app,
    dispatch_uid="django.contrib.auth.management.create_superuser")


class Permissions:
    #keep in sync
    PREFIX = 'docapproval'

    @classmethod
    def _(cls, permission, app_label='DocApproval'):
        """Adds app_label to requested permission"""
        return app_label + "." + permission

    class Request:
        #django permissions (applied at model class level)
        CAN_CREATE_REQUESTS = "docapproval_can_create_requests"
        CAN_APPROVE_REQUESTS = "docapproval_can_approve_requests"
        CAN_VIEW_ALL_REQUESTS = "docapproval_can_view_all_requests"
        #guardian permissions (applied per model instance => shouldn't be shown in admin)
        CAN_VIEW_REQUEST = "guardian_can_view_request"

    class UserProfile:
        CAN_CHANGE_POSITION = "docapproval_can_change_position"
        CAN_CHANGE_MANAGER = "docapproval_can_change_manager"

        CAN_CHANGE_ANY_POSITION = "docapproval_can_change_any_position"
        CAN_CHANGE_ANY_MANAGER = "docapproval_can_change_any_manager"

    class ApprovalRoute:
        CAN_MANAGE_TEMPLATES = "docapproval_can_create_templates"


class ModelConstants:
    MAX_NAME_LENGTH = 500
    MAX_VARCHAR_LENGTH = 4000
    DEFAULT_VARCHAR_LENGTH = 800
    MAX_CODE_VARCHAR_LENGTH = 50


class NonTemplateApprovalRouteException(Exception):
    pass


#Some "dictionaries" first
class Position(models.Model):
    position_name = models.CharField(_(u'Должность'), max_length=ModelConstants.MAX_VARCHAR_LENGTH)

    class Meta:
        verbose_name = _(u'Должность')
        verbose_name_plural = _(u'Должности')

    def __unicode__(self):
        return self.position_name


class City(models.Model):
    city_name = models.CharField(_(u'Название города'), max_length=ModelConstants.MAX_VARCHAR_LENGTH)

    class Meta:
        verbose_name = _(u'Город')
        verbose_name_plural = _(u'Города')

    def __unicode__(self):
        return self.city_name


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
        verbose_name = _(u'Статус заявки')
        verbose_name_plural = _(u'Статусы заявок')

    def __unicode__(self):
        return self.status_name


#Primary objects
class UserProfile(models.Model):
    def upload_to(self, filename):
        fname, fext = os.path.splitext(filename)
        return u'signs/{0}/sign.{1}'.format(self.pk, fext)

    user = models.OneToOneField(User, primary_key=True, verbose_name=_(u'Учетная запись'), related_name='profile')
    last_name = models.CharField(_(u'Фамилия'), max_length=ModelConstants.MAX_NAME_LENGTH)
    first_name = models.CharField(_(u'Имя'), max_length=ModelConstants.MAX_NAME_LENGTH)
    middle_name = models.CharField(_(u'Отчество'), max_length=ModelConstants.MAX_NAME_LENGTH)

    last_name_accusative = models.CharField(_(u'Фамилия (вин.)'), max_length=ModelConstants.MAX_NAME_LENGTH, blank=True,
                                            null=True)
    first_name_accusative = models.CharField(_(u'Имя (вин.)'), max_length=ModelConstants.MAX_NAME_LENGTH, blank=True,
                                             null=True)
    middle_name_accusative = models.CharField(_(u'Отчество (вин.)'), max_length=ModelConstants.MAX_NAME_LENGTH,
                                              blank=True, null=True)

    sign = models.ImageField(_(u'Подпись'), max_length=ModelConstants.DEFAULT_VARCHAR_LENGTH, upload_to=upload_to,
                             blank=True, null=True)
    email = models.EmailField(_(u'Email'), max_length=ModelConstants.DEFAULT_VARCHAR_LENGTH)
    position = models.ForeignKey(Position, verbose_name=_(u'Должность'))
    manager = models.ForeignKey('self', verbose_name=_(u'Руководитель'), blank=True, null=True)
    city = models.ForeignKey(City, verbose_name=_(u"Город"), blank=False, null=False)

    def get_absolute_url(self):
        return reverse(ProfileUrls.PROFILE, kwargs={'pk': self.pk})

    def get_full_name(self):
        return u"{0} {1} {2}".format(self.last_name, self.first_name, self.middle_name)

    def get_short_name(self):
        return u"{0} {1}".format(self.last_name, self.first_name)

    def get_full_name_accusative(self):
        #gets accusative full name, falls back to using subjective case if accusatives is empty
        eff_first_accusative = self.first_name_accusative if self.first_name_accusative else self.first_name
        eff_last_accusative = self.last_name_accusative if self.last_name_accusative else self.last_name
        eff_middle_accusative = self.middle_name_accusative if self.middle_name_accusative else self.middle_name
        return "{0} {1} {2}".format(eff_last_accusative, eff_first_accusative, eff_middle_accusative)

    def __unicode__(self):
        return u"{0} ({1})".format(self.get_full_name(), self.position)

    class Meta:
        verbose_name = _(u'Пользовательские данные')
        verbose_name_plural = _(u'Пользовательские данные')
        permissions = (
            (Permissions.UserProfile.CAN_CHANGE_POSITION, _(u"Может изменять должность")),
            (Permissions.UserProfile.CAN_CHANGE_MANAGER, _(u"Может изменять руководителя")),

            (Permissions.UserProfile.CAN_CHANGE_ANY_POSITION, _(u"Может изменять должность других пользователей")),
            (Permissions.UserProfile.CAN_CHANGE_ANY_MANAGER, _(u"Может изменять руководителя других пользователей")),
        )


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
        verbose_name = _(u"Документ")
        verbose_name_plural = _(u"Документы")

    def active_period_humanize(self):
        return Humanizer().humanize_days(self.active_period)


class ApprovalRoute(models.Model):
    DIRECT_MANAGER_PLACEHOLDER = '{manager}'
    REQUEST_ROUTE_NAMING_TEMPLATE = _(u"Маршрут утверждения заявки {0}")

    name = models.CharField(_(u"Название"), max_length=ModelConstants.MAX_NAME_LENGTH)
    description = models.CharField(_(u"Описание"), max_length=ModelConstants.MAX_VARCHAR_LENGTH, default='')

    created = models.DateField(_(u"Создан"), auto_now_add=True)
    modified = models.DateField(_(u"Последнее изменение"), auto_now=True)

    is_template = models.BooleanField(_(u"Шаблонный маршрут"), default=False)

    def roll_template_route(self):
        if not self.is_template:
            raise NonTemplateApprovalRouteException("Current route is not a template route")
        else:
            raise NotImplementedError("Not implemented yet")

    class Meta:
        permissions = (
            (Permissions.ApprovalRoute.CAN_MANAGE_TEMPLATES, _(u"Может создавать шаблонные маршруты")),
        )

    @classmethod
    @transaction.commit_on_success
    def create_or_update_with_steps(cls, pk=None, name=None, description=None, is_template=False, steps=None):
        primary_key = pk if pk and int(pk) else None
        route, created = ApprovalRoute.objects.get_or_create(
            pk=primary_key,
            defaults={'name': name, 'description': description, 'is_template': is_template}
        )
        if not created:
            route.name = name
            route.description = description
            if route.is_template != is_template:
                raise ValueError(
                    "Can't make template route non-template and vice versa. Template was {0}, tried to make it {1}".format(
                        route.is_template, is_template))

        route.save()

        steps_to_keep = []
        for step_number, approvers in steps.iteritems():
            route.add_step(step_number, set(approvers))
            steps_to_keep.append(int(step_number))

        route.remove_steps(steps_to_keep)

        return route

    def add_step(self, step_number, approvers):
        if not isinstance(approvers, set) or not approvers:
            raise ValueError("Approvers parameter must be a non-empty set")

        existing_approvers_in_step = set(step.approver.pk for step in self.steps.filter(step_number=step_number))
        approvers_to_add = approvers - existing_approvers_in_step
        approvers_to_remove = existing_approvers_in_step - approvers

        for approver_id in approvers_to_add:
            approver = User.objects.get(pk=approver_id)
            self.steps.create(approver=approver.profile, step_number=step_number)
            if self.request:
                assign_perm(Permissions._(Permissions.Request.CAN_VIEW_REQUEST), approver, self.request)

        if self.request:
            for approver_id in approvers_to_remove:
                approver = User.objects.get(pk=approver_id)
                remove_perm(Permissions._(Permissions.Request.CAN_VIEW_REQUEST), approver, self.request)

        self.steps.filter(approver__pk__in=approvers_to_remove).delete()

    def remove_steps(self, steps_to_keep):
        to_remove = self.steps.exclude(step_number__in=steps_to_keep)
        if self.request:
            for step in to_remove:
                approver = User.objects.get(pk=step.approver.pk)
                remove_perm(Permissions._(Permissions.Request.CAN_VIEW_REQUEST), approver, self.request)

        to_remove.delete()

    def get_steps_count(self):
        return self.steps.all().aggregate(models.Max('step_number')).get('step_number__max')


class ApprovalRouteStep(models.Model):
    route = models.ForeignKey(ApprovalRoute, verbose_name=_(u"Маршрут утверждения"), related_name='steps')
    approver = models.ForeignKey(UserProfile, verbose_name=_(u"Утверждающий"))
    step_number = models.IntegerField(verbose_name=_(u"Номер шага"))


class RequestManager(models.Manager):
    target_permissions = (
        Permissions.Request.CAN_VIEW_REQUEST,
        Permissions.Request.CAN_VIEW_ALL_REQUESTS
    )

    def get_accessible_requests(self, user):
        return get_objects_for_user(user, self.target_permissions, klass=Request, any_perm=True)

    def get_awaiting_approval(self, user):
        return self.get_accessible_requests(user).filter(approval_route__steps__approver=user)


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

    comments = models.CharField(_(u'Комментарии'), max_length=ModelConstants.MAX_VARCHAR_LENGTH, null=True, blank=True)

    class Meta:
        verbose_name = _(u'Заявка')
        verbose_name_plural = _(u'Заявки')
        permissions = (
            (Permissions.Request.CAN_CREATE_REQUESTS, _(u"Может создавать запросы на утверждение")),
            (Permissions.Request.CAN_APPROVE_REQUESTS, _(u"Может утверждать документы")),
            (Permissions.Request.CAN_VIEW_ALL_REQUESTS, _(u"Может просматривать любые заявки")),

            (Permissions.Request.CAN_VIEW_REQUEST, _(u"Имеет доступ к данной заявке"))
        )

    def get_absolute_url(self):
        return reverse(RequestUrls.DETAILS, kwargs={'pk': self.pk})

    def __unicode__(self):
        return u"{0} {2} {1} {3}".format(_(u"Заявка"), _(u"от"), self.name, self.created)

    def get_initiator(self):
        return self.creator

    def get_approvers(self):
        return (step.approver for step in self.approval_route.steps)

    def accessible_by(self, user):
        return (
            self.creator == user.profile or
            user.has_perm(Permissions._(Permissions.Request.CAN_VIEW_ALL_REQUESTS)) or
            (self.approval_route and self.approval_route.steps.exists(approver__exact=user.profile))
        )


class ApprovalProcess(models.Model):
    route = models.ForeignKey(ApprovalRoute, verbose_name=_(u"Маршрут"), related_name='processes')
    attempt_number = models.IntegerField(_(u"Попытка утверждения №"))
    is_current = models.BooleanField(_(u"Текущий процесс"))


class ApprovalProcessAction(models.Model):
    ACTION_APPROVE = 'approve'
    ACTION_REJECT = 'reject'
    step = models.ForeignKey(ApprovalRouteStep, verbose_name=_(u"Шаг утверждения"))
    action = models.CharField(_(u"Действие"), max_length=ModelConstants.MAX_CODE_VARCHAR_LENGTH)

    action_taken = models.DateTimeField(_(u"Время принятия решения"))
    actor = models.ForeignKey(UserProfile, verbose_name=_(u"Кто принял решение"))


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

        return new_request

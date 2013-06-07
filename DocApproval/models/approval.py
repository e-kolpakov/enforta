#-*- coding: utf-8 -*-
import logging

from django.db import models, transaction
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.dispatch.dispatcher import Signal
from django.utils.translation import ugettext as _

from guardian.shortcuts import assign_perm, remove_perm

from .user import UserProfile
from .common import ModelConstants, Permissions

from DocApproval.url_naming.names import ApprovalRoute as ApprovalRouteUrls

_logger = logging.getLogger(__name__)


class LoggerMessages(object):
    REQUEST_APPROVED = u"User {0} set final approve on request {1} on behalf of {2}"
    REQUEST_REJECTED = u"User {0} rejected request {1} on behalf of {2}"


class NonTemplateApprovalRouteException(Exception):
    pass


class ApprovalRoute(models.Model):
    REQUEST_ROUTE_NAMING_TEMPLATE = _(u"Маршрут утверждения заявки {0}")

    name = models.CharField(_(u"Название"), max_length=ModelConstants.MAX_NAME_LENGTH)
    description = models.CharField(_(u"Описание"), max_length=ModelConstants.MAX_VARCHAR_LENGTH, default='')

    created = models.DateField(_(u"Создан"), auto_now_add=True)
    modified = models.DateField(_(u"Последнее изменение"), auto_now=True)

    is_template = models.BooleanField(_(u"Шаблонный маршрут"), default=False)

    class Meta:
        verbose_name = _(u"Маршрут утверждения")
        verbose_name_plural = _(u"Маршруты утверждения")
        app_label = "DocApproval"
        permissions = (
            (Permissions.ApprovalRoute.CAN_MANAGE_TEMPLATES, _(u"Может создавать шаблонные маршруты")),
        )

    def get_absolute_url(self):
        return reverse(ApprovalRouteUrls.UPDATE, kwargs={'pk': self.pk})

    def __unicode__(self):
        return self.name

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

        route.remove_steps(exclude=steps_to_keep)

        return route

    def add_step(self, step_number, approvers):
        if not isinstance(approvers, set) or not approvers:
            raise ValueError("Approvers parameter must be a non-empty set")

        incoming_approvers = set(User.objects.filter(pk__in=approvers))
        existing_approvers_in_step = set(step.approver.user for step in self.steps.filter(step_number=step_number))
        approvers_to_add = incoming_approvers - existing_approvers_in_step
        approvers_to_remove = existing_approvers_in_step - incoming_approvers

        for approver in approvers_to_add:
            self.steps.create(approver=approver.profile, step_number=step_number)

        self.process_request_permissions(to_add=approvers_to_add, to_remove=approvers_to_remove)

        self.steps.filter(approver__user__in=approvers_to_remove).delete()

    def remove_steps(self, exclude=None):
        steps_to_remove = self.steps.exclude(step_number__in=exclude).select_related('approver')
        users_to_remove_permissions = [step.approver.user for step in steps_to_remove]
        self.process_request_permissions(to_remove=users_to_remove_permissions)

        steps_to_remove.delete()

    def process_request_permissions(self, to_remove=None, to_add=None):
        if self.is_template:
            return

        for approver in (to_remove or []):
            remove_perm(Permissions._(Permissions.Request.CAN_VIEW_REQUEST), approver, self.request)

        for approver in (to_add or []):
            assign_perm(Permissions._(Permissions.Request.CAN_VIEW_REQUEST), approver, self.request)

    def get_steps_count(self):
        return self.steps.all().aggregate(models.Max('step_number')).get('step_number__max')

    def get_current_approvers(self):
        try:
            active_step_number = self.processes.get(is_current=True).current_step_number
        except ApprovalProcess.DoesNotExist:
            active_step_number = ApprovalProcess.STARTING_STEP_NUMBER
        return [step.approver for step in self.steps.filter(step_number=active_step_number)]

    def get_current_process(self):
        try:
            return self.processes.get(is_current=True)
        except ApprovalProcess.DoesNotExist:
            _logger.warning(
                "Tried to get current approval process for route {0} no current approval process exist".format(self))
            return None


class ApprovalRouteStep(models.Model):
    DIRECT_MANAGER_PLACEHOLDER = '{manager}'

    route = models.ForeignKey(ApprovalRoute, verbose_name=_(u"Маршрут утверждения"), related_name='steps')
    approver = models.ForeignKey(UserProfile, verbose_name=_(u"Утверждающий"), null=True, related_name='approval_steps')
    step_number = models.IntegerField(verbose_name=_(u"Номер шага"))
    calc_step = models.CharField(
        verbose_name=_(u"Вычисляемый утверждающий"), null=True, blank=True, default=None,
        max_length=ModelConstants.MAX_CODE_VARCHAR_LENGTH,
        choices=((DIRECT_MANAGER_PLACEHOLDER, _(u"Непосредственный руководитель")),)
    )

    class Meta:
        app_label = "DocApproval"


class ApprovalProcess(models.Model):
    STARTING_STEP_NUMBER = 1
    route = models.ForeignKey(ApprovalRoute, verbose_name=_(u"Маршрут"), related_name='processes')
    attempt_number = models.IntegerField(_(u"Попытка утверждения №"))
    is_current = models.BooleanField(_(u"Текущий процесс"))
    is_successful = models.BooleanField(_(u"Завершился успешно"), default=False),
    current_step_number = models.IntegerField(verbose_name=_(u"Текущий шаг"), default=STARTING_STEP_NUMBER, null=False)

    class Meta:
        app_label = "DocApproval"

    @transaction.commit_on_success
    def step_approved(self, user_profile, approver, comment=None):
        self._process_action(user_profile, ApprovalProcessAction.ACTION_APPROVE, comment, approver)
        approve_signal.send(ApprovalProcess, request_pk=self.route.request.pk, user_pk=user_profile.pk)
        if self.current_step_number != self.route.get_steps_count():
            self.current_step_number += 1
            self.save()
        else:
            _logger.info(LoggerMessages.REQUEST_APPROVED.format(user_profile, self.route.request, approver))
            final_approve_signal.send(ApprovalProcess, request_pk=self.route.request.pk, user_pk=user_profile.pk)

    @transaction.commit_on_success
    def step_rejected(self, user_profile, approver, comment=None):
        _logger.info(LoggerMessages.REQUEST_REJECTED.format(user_profile, self.route.request, approver))
        self._process_action(user_profile, ApprovalProcessAction.ACTION_REJECT, comment, approver)
        reject_signal.send(ApprovalProcess, request_pk=self.route.request.pk, user_pk=user_profile.pk)

    def _process_action(self, user_profile, action_code, comment, approver):
        current_step = self.current_step_number
        step = self.route.steps.get(approver=approver, step_number=current_step)

        ApprovalProcessAction.objects.create(process=self, step=step, action=action_code, comment=comment,
                                             actor=user_profile)


class ApprovalProcessAction(models.Model):
    ACTION_APPROVE = 'approve'
    ACTION_REJECT = 'reject'
    process = models.ForeignKey(ApprovalProcess, verbose_name=_(u"Попытка утверждения"), related_name='actions')
    step = models.ForeignKey(ApprovalRouteStep, verbose_name=_(u"Шаг утверждения"))
    action = models.CharField(
        _(u"Действие"), max_length=ModelConstants.MAX_CODE_VARCHAR_LENGTH, null=False,
        choices=((ACTION_APPROVE, _(u"Утвердить")), (ACTION_REJECT, _(u"Отклонить")),)
    )

    comment = models.CharField(max_length=ModelConstants.MAX_VARCHAR_LENGTH, verbose_name=_(u"Комментарий"), null=True,
                               blank=True)
    action_taken = models.DateTimeField(_(u"Время принятия решения"), auto_now_add=True)
    actor = models.ForeignKey(UserProfile, verbose_name=_(u"Кто принял решение"))

    class Meta:
        app_label = "DocApproval"

    def get_action_display_past_form(self):
        return {
            self.ACTION_APPROVE: _(u"Утверждена"),
            self.ACTION_REJECT: _(u"Отклонена")
        }.get(self.action, _(u"Действие неизвестно"))


approve_signal = Signal(providing_args=(['request_pk', 'user_pk']))
final_approve_signal = Signal(providing_args=(['request_pk', 'user_pk']))
reject_signal = Signal(providing_args=(['request_pk', 'user_pk']))
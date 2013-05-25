#-*- coding: utf-8 -*-
from django.db import models, transaction
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from guardian.shortcuts import assign_perm, remove_perm

from .user import UserProfile
from .common import ModelConstants, Permissions

from DocApproval.url_naming.names import ApprovalRoute as ApprovalRouteUrls


class NonTemplateApprovalRouteException(Exception):
    pass


class ApprovalRoute(models.Model):
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

    def get_current_reviewers(self):
        try:
            active_step_number = self.processes.get(is_current=True).current_step_number
        except ApprovalProcess.DoesNotExist:
            active_step_number = ApprovalProcess.STARTING_STEP_NUMBER
        return [step.approver for step in self.steps.filter(step_number=active_step_number)]


class ApprovalRouteStep(models.Model):
    DIRECT_MANAGER_PLACEHOLDER = '{manager}'

    route = models.ForeignKey(ApprovalRoute, verbose_name=_(u"Маршрут утверждения"), related_name='steps')
    approver = models.ForeignKey(UserProfile, verbose_name=_(u"Утверждающий"), null=True)
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
    current_step_number = models.IntegerField(verbose_name=_(u"Текущий шаг"), default=STARTING_STEP_NUMBER)

    class Meta:
        app_label = "DocApproval"


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
    action_taken = models.DateTimeField(_(u"Время принятия решения"))
    actor = models.ForeignKey(UserProfile, verbose_name=_(u"Кто принял решение"))

    class Meta:
        app_label = "DocApproval"



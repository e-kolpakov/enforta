#-*- coding: utf-8 -*-
import logging

from django.db import models, transaction
from django.core.urlresolvers import reverse
from django.dispatch.dispatcher import Signal
from django.utils.translation import ugettext as _

from guardian.shortcuts import assign_perm, remove_perm
from DocApproval.utilities.utility import wrap_permission

from .user import UserProfile
from .common import ModelConstants, Permissions
from ..messages import ApprovalRouteMessages

from DocApproval.url_naming.names import ApprovalRoute as ApprovalRouteUrls

_logger = logging.getLogger(__name__)


class LoggerMessages(object):
    REQUEST_APPROVED = u"User {0} set final approve on request {1} on behalf of {2}"
    REQUEST_REJECTED = u"User {0} rejected request {1} on behalf of {2}"


class ApprovalRouteExceptionBase(Exception):
    ui_msg = ""

    def __init__(self, *args, **kwargs):
        super(ApprovalRouteExceptionBase, self).__init__(*args, **kwargs)

    @property
    def message(self):
        return super(ApprovalRouteExceptionBase, self).message

    @property
    def ui_message(self):
        return self.ui_msg


class NonTemplateApprovalRouteException(ApprovalRouteExceptionBase):
    MESSAGE_TEMPLATE = "Can't make template route non-template and vice versa. Route was {0}, tried to make it {1}"

    ui_msg = ApprovalRouteMessages.NON_EDITABLE_ROUTE_MESSAGE

    def __init__(self, old_val, new_val, *args, **kwargs):
        self.old_val = old_val
        self.new_val = new_val
        super(NonTemplateApprovalRouteException, self).__init__(*args, **kwargs)

    def _yes_no(self, value):
        return "template" if value else "non-template"

    @property
    def message(self):
        return self.MESSAGE_TEMPLATE.format(self._yes_no(self.old_val), self._yes_no(self.new_val))


class ApprovalRouteModificationException(ApprovalRouteExceptionBase):
    ui_msg = ApprovalRouteMessages.ROUTE_TEMPLATE_SWITCH_NOT_ALLOWED


class EmptyStepsValueError(ValueError, ApprovalRouteExceptionBase):
    ui_msg = ApprovalRouteMessages.EMPTY_ROUTE_STEPS


class NoManager(ApprovalRouteExceptionBase):
    ui_msg = ApprovalRouteMessages.NO_MANAGER


class UnavailableInTemplate(ApprovalRouteExceptionBase):
    def __init__(self, method_name, *args, **kwargs):
        self.ui_msg = ApprovalRouteMessages.NON_AVAILABLE_FOR_TEMPLATE.format(method_name)
        super(UnavailableInTemplate, self).__init__(*args, **kwargs)


class ApprovalRoute(models.Model):
    REQUEST_ROUTE_NAMING_TEMPLATE = _(u"Маршрут утверждения заявки {0}")
    emit_changed_signal = True

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

    def __init__(self, *args, **kwargs):
        self.is_template = False
        super(ApprovalRoute, self).__init__(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(ApprovalRouteUrls.UPDATE, kwargs={'pk': self.pk})

    def __unicode__(self):
        return self.name

    def update_parameters(self, name, description):
        self.name = name
        self.description = description
        self.save()

    def set_steps(self, user, steps=None):
        if not steps:
            raise EmptyStepsValueError("Incorrect steps list")

        steps_to_keep = []
        for step_number, approvers in steps.iteritems():
            self.add_step(step_number, set(approvers), user)
            steps_to_keep.append(int(step_number))

        self.remove_steps(exclude=steps_to_keep)
        if self.emit_changed_signal:
            approval_route_changed_signal.send(ApprovalRoute, request=self.request, user=user)

    def _get_existing_approver_pks(self, step_number):
        return set(
            step.approver.pk
            for step in self.steps.filter(step_number=step_number, approver__isnull=False).select_related('approver'))

    def _get_processing_lists(self, step_number, incoming_approvers):
        existing_approvers_in_step = self._get_existing_approver_pks(step_number=step_number)
        approvers_to_add_pks = incoming_approvers - existing_approvers_in_step
        approvers_to_remove_pks = existing_approvers_in_step - incoming_approvers
        return approvers_to_add_pks, approvers_to_remove_pks

    def _fetch_template_approver(self, template_approver, user):
        # TODO: if the template list grows bigger than two - refactor into strategy pattern
        if template_approver == ApprovalRouteStep.DIRECT_MANAGER:
            if user.manager:
                return user.manager.pk
            else:
                raise NoManager()

    def add_step(self, step_number, approvers, user):
        if not isinstance(approvers, set) or not approvers:
            raise ValueError("Approvers parameter must be a non-empty set")

        approvers_to_add_pks, approvers_to_remove_pks = self._get_processing_lists(step_number, approvers)
        rolled_template_approvers = set([
            self._fetch_template_approver(approver, user)
            for approver in approvers_to_add_pks if approver < 0
        ])
        approvers_to_add_pks = approvers_to_add_pks | rolled_template_approvers
        approvers_to_add = UserProfile.objects.filter(pk__in=approvers_to_add_pks).select_related('user')
        approvers_to_remove = UserProfile.objects.filter(pk__in=approvers_to_remove_pks).select_related('user')

        for approver in approvers_to_add:
            self.steps.create(approver=approver, step_number=step_number)

        self.steps.filter(approver__user__in=approvers_to_remove, step_number=step_number).delete()
        self.process_request_permissions(to_add=approvers_to_add, to_remove=approvers_to_remove)

    def remove_steps(self, exclude=None):
        steps_to_remove = self.steps.exclude(step_number__in=exclude).select_related('approver__user')
        users_to_remove_permissions = [step.approver for step in steps_to_remove]
        self.process_request_permissions(to_remove=users_to_remove_permissions)

        steps_to_remove.delete()

    def process_request_permissions(self, to_remove=None, to_add=None):
        if self.is_template:
            return

        for approver in (to_remove or []):
            remove_perm(wrap_permission(Permissions.Request.CAN_VIEW_REQUEST), approver.user, self.request)

        for approver in (to_add or []):
            assign_perm(wrap_permission(Permissions.Request.CAN_VIEW_REQUEST), approver.user, self.request)

    def get_steps_count(self):
        return self.steps.all().aggregate(models.Max('step_number')).get('step_number__max')

    def get_approvers(self, step_number):
        return [step.approver for step in self.steps.filter(step_number=step_number)]

    def get_current_approvers(self):
        current_process = self.processes.get(is_current=True)
        step_number = current_process.current_step_number if current_process else ApprovalProcess.STARTING_STEP_NUMBER
        return self.get_approvers(step_number)

    def get_current_process(self):
        try:
            return self.processes.get(is_current=True)
        except ApprovalProcess.DoesNotExist:
            _logger.warning(
                "Tried to get current approval process for route {0}, no current approval process exist".format(self))
            return None

    def get_successful_process(self):
        return self.processes.get(is_successful=True)


class TemplateApprovalRoute(ApprovalRoute):
    emit_changed_signal = False

    class Meta:
        app_label = "DocApproval"
        proxy = True

    def __init__(self, *args, **kwargs):
        super(ApprovalRoute, self).__init__(*args, **kwargs)
        self.is_template = True

    def _get_existing_approver_pks(self, step_number):
        approvers = super(TemplateApprovalRoute, self)._get_existing_approver_pks(step_number)
        template_approvers = set(
            step.calc_step
            for step in self.steps.filter(step_number=step_number, approver__isnull=True))
        return approvers | template_approvers

    def _process_template_approvers(self, step_number, to_add, to_remove):
        template_approvers_to_add = [
            approver for approver in to_add
            if approver < 0 and approver in ApprovalRouteStep.allowed_templates
        ]
        template_approvers_to_remove = [approver for approver in to_remove if approver < 0]

        self.steps.filter(calc_step__in=template_approvers_to_remove, step_number=step_number).delete()

        for template in template_approvers_to_add:
            self.steps.create(calc_step=template, step_number=step_number)

    def add_step(self, step_number, approvers, user):
        if not isinstance(approvers, set) or not approvers:
            raise ValueError("Approvers parameter must be a non-empty set")

        approvers_to_add_pks, approvers_to_remove_pks = self._get_processing_lists(step_number, set(approvers))
        approvers_to_add = UserProfile.objects.filter(pk__in=approvers_to_add_pks)
        approvers_to_remove = UserProfile.objects.filter(pk__in=approvers_to_remove_pks)

        for approver in approvers_to_add:
            self.steps.create(approver=approver, step_number=step_number)

        self.steps.filter(approver__user__in=approvers_to_remove, step_number=step_number).delete()
        self._process_template_approvers(step_number, approvers_to_add_pks, approvers_to_remove_pks)

    def remove_steps(self, exclude=None):
        self.steps.exclude(step_number__in=exclude).delete()

    def process_request_permissions(self, to_remove=None, to_add=None):
        raise UnavailableInTemplate(_(u"Установка прав доступа к заявке"))

    def get_approvers(self):
        raise UnavailableInTemplate(_(u"Текущие утверждающие"))

    def get_current_process(self):
        raise UnavailableInTemplate(_(u"Текущий процесс утверждения"))

    def get_successful_process(self):
        raise UnavailableInTemplate(_(u"Успешный процесс утверждения"))


class ApprovalRouteStep(models.Model):
    DIRECT_MANAGER = -1
    DIRECT_MANAGER_CAPTION = _(u"Непосредственный руководитель")

    allowed_templates = (DIRECT_MANAGER, )

    route = models.ForeignKey(ApprovalRoute, verbose_name=_(u"Маршрут утверждения"), related_name='steps')
    approver = models.ForeignKey(UserProfile, verbose_name=_(u"Утверждающий"), null=True, related_name='approval_steps')
    step_number = models.IntegerField(verbose_name=_(u"Номер шага"))
    calc_step = models.IntegerField(
        verbose_name=_(u"Вычисляемый утверждающий"), null=True, blank=True, default=None,
        choices=((DIRECT_MANAGER, DIRECT_MANAGER_CAPTION),)
    )

    class Meta:
        app_label = "DocApproval"

    @property
    def key(self):
        return self.calc_step if self.calc_step else self.approver.pk


class ApprovalProcess(models.Model):
    STARTING_STEP_NUMBER = 1
    route = models.ForeignKey(ApprovalRoute, verbose_name=_(u"Маршрут"), related_name='processes')
    attempt_number = models.IntegerField(_(u"Попытка утверждения №"))
    is_current = models.BooleanField(_(u"Текущий процесс"))
    is_successful = models.BooleanField(_(u"Завершился успешно"), default=False)
    current_step_number = models.IntegerField(verbose_name=_(u"Текущий шаг"), default=STARTING_STEP_NUMBER, null=False)

    class Meta:
        app_label = "DocApproval"

    @transaction.commit_on_success
    def step_approved(self, user_profile, approver, comment=None):
        self._process_action(user_profile, ApprovalProcessAction.ACTION_APPROVE, comment, approver)
        self.send_action_signal(ApprovalProcessAction.ACTION_APPROVE, user_profile, approver, comment)

        if self.current_step_number != self.route.get_steps_count():
            self.current_step_number += 1
            self.save()
        else:
            self.is_successful = True
            self.save()
            self.send_action_signal(ApprovalProcessAction.ACTION_FINAL_APPROVE, user_profile, approver, comment)
            _logger.info(LoggerMessages.REQUEST_APPROVED.format(user_profile, self.route.request, approver))

    @transaction.commit_on_success
    def step_rejected(self, user_profile, approver, comment=None):
        _logger.info(LoggerMessages.REQUEST_REJECTED.format(user_profile, self.route.request, approver))
        self._process_action(user_profile, ApprovalProcessAction.ACTION_REJECT, comment, approver)
        self.send_action_signal(ApprovalProcessAction.ACTION_REJECT, user_profile, approver, comment)

    def send_action_signal(self, action_type, user_profile, approver, comment):
        approve_action_signal.send(
            ApprovalProcess, request=self.route.request, user=user_profile, on_behalf_of=approver, comment=comment,
            action_type=action_type, step_number=self.current_step_number)

    def _process_action(self, user_profile, action_code, comment, approver):
        current_step = self.current_step_number
        step = self.route.steps.get(approver=approver, step_number=current_step)

        ApprovalProcessAction.objects.create(process=self, step=step, action=action_code, comment=comment,
                                             actor=user_profile)

    def get_approval_actions(self):
        return self.actions.all().select_related('step__approver__profile')

    def get_approval_action(self, user):
        try:
            all_actions = self.actions.filter(step__approver=user) \
                .order_by('-step__step_number').select_related('step__approver__profile')
            last_action = all_actions[0]
        except IndexError: # no actions taken
            last_action = None
        return last_action


class ApprovalProcessAction(models.Model):
    ACTION_APPROVE = 'approve'
    ACTION_REJECT = 'reject'
    ACTION_FINAL_APPROVE = 'final_approve'
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


approve_action_signal = Signal(
    providing_args=(['request', 'user', 'on_behalf_of', 'comment', 'action_type', 'step_number'])
)
approval_route_changed_signal = Signal(providing_args=(['request', 'user']))
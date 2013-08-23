#-*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext as _


class ModelConstants:
    MAX_NAME_LENGTH = 500
    MAX_VARCHAR_LENGTH = 4000
    DEFAULT_VARCHAR_LENGTH = 800
    MAX_CODE_VARCHAR_LENGTH = 50


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
        CAN_EDIT_REQUEST = "guardian_can_edit_request"
        CAN_EDIT_ROUTE = "guardian_can_edit_route"

        CAN_SET_PAID_DATE = "docapproval_can_set_edit_date"

    class UserProfile:
        CAN_CHANGE_POSITION = "docapproval_can_change_position"
        CAN_CHANGE_MANAGER = "docapproval_can_change_manager"

        CAN_CHANGE_ANY_POSITION = "docapproval_can_change_any_position"
        CAN_CHANGE_ANY_MANAGER = "docapproval_can_change_any_manager"

    class ApprovalRoute:
        CAN_MANAGE_TEMPLATES = "docapproval_can_create_templates"

    class TemplateUserReplacements:
        CAN_MANAGE_REPLACEMENTS = "docapproval_can_manage_replacements"


class Position(models.Model):
    position_name = models.CharField(_(u'Должность'), max_length=ModelConstants.MAX_VARCHAR_LENGTH)

    class Meta:
        app_label = "DocApproval"
        verbose_name = _(u'Должность')
        verbose_name_plural = _(u'Должности')

    def __unicode__(self):
        return self.position_name


class City(models.Model):
    name = models.CharField(_(u'Название города'), max_length=ModelConstants.MAX_VARCHAR_LENGTH)

    class Meta:
        app_label = "DocApproval"
        verbose_name = _(u'Город')
        verbose_name_plural = _(u'Города')

    def __unicode__(self):
        return self.name


class DepartmentManager(models.Manager):
    def get_departments_for_list(self, city):
        return self.filter(city=city, show_in_list=True).select_related('responsible_user')


class Department(models.Model):
    objects = DepartmentManager()

    name = models.CharField(_(u'Дирекция'), max_length=ModelConstants.MAX_VARCHAR_LENGTH)
    city = models.ForeignKey(City, verbose_name=_(u'Город'))
    show_in_list = models.BooleanField(verbose_name=_(u'Отображать в листе утверждения'), default=False)
    #avoiding circular reference by using model name as a string
    responsible_user = models.ForeignKey('UserProfile', verbose_name=_(u'Ответственный'), null=True, blank=True)

    class Meta:
        app_label = "DocApproval"
        verbose_name = _(u'Дирекция')
        verbose_name_plural = _(u'Дирекции')

    def __unicode__(self):
        return u'{0}({1})'.format(self.name, self.city.name)


class Currency(models.Model):
    caption = models.CharField(_(u'Наименование'), max_length=ModelConstants.DEFAULT_VARCHAR_LENGTH)
    caption_plural = models.CharField(_(u'Множественное число'), max_length=ModelConstants.DEFAULT_VARCHAR_LENGTH)
    short_caption = models.CharField(_(u'Сокращенное наименование'), max_length=ModelConstants.DEFAULT_VARCHAR_LENGTH)
    symbol = models.CharField(_(u'Символ'), max_length=ModelConstants.MAX_CODE_VARCHAR_LENGTH)

    class Meta:
        app_label = "DocApproval"
        verbose_name = _(u'Валюта')
        verbose_name_plural = _(u'Валюты')

    def __unicode__(self):
        return self.caption_plural
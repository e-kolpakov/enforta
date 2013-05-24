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

    class UserProfile:
        CAN_CHANGE_POSITION = "docapproval_can_change_position"
        CAN_CHANGE_MANAGER = "docapproval_can_change_manager"

        CAN_CHANGE_ANY_POSITION = "docapproval_can_change_any_position"
        CAN_CHANGE_ANY_MANAGER = "docapproval_can_change_any_manager"

    class ApprovalRoute:
        CAN_MANAGE_TEMPLATES = "docapproval_can_create_templates"


#Some "dictionaries" first
class Position(models.Model):
    position_name = models.CharField(_(u'Должность'), max_length=ModelConstants.MAX_VARCHAR_LENGTH)

    class Meta:
        app_label = "DocApproval"
        verbose_name = _(u'Должность')
        verbose_name_plural = _(u'Должности')

    def __unicode__(self):
        return self.position_name


class City(models.Model):
    city_name = models.CharField(_(u'Название города'), max_length=ModelConstants.MAX_VARCHAR_LENGTH)

    class Meta:
        app_label = "DocApproval"
        verbose_name = _(u'Город')
        verbose_name_plural = _(u'Города')

    def __unicode__(self):
        return self.city_name
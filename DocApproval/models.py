#-*- coding: utf-8 -*-
import re
from datetime import timedelta

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _


class ModelConstants:
    MAX_NAME_LENGTH = 500
    MAX_VARCHAR_LENGTH = 4000
    DEFAULT_VARCHAR_LENGTH = 800
    MAX_CODE_VARCHAR_LENGTH = 50


#Some "dictionaries" first
class Position(models.Model):
    position_name = models.CharField(_(u'Должность'), max_length=ModelConstants.MAX_VARCHAR_LENGTH)

    class Meta:
        verbose_name = _(u'Должность')
        verbose_name_plural = _(u'Должности')
        permissions = (
            ("docapproval.can_change_position", _(u"Может изменять должность")),
        )

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
    code = models.CharField(_(u'Код'), max_length=ModelConstants.MAX_CODE_VARCHAR_LENGTH, primary_key=True,
                            editable=False)
    status_name = models.CharField(_(u'Статус'), max_length=ModelConstants.DEFAULT_VARCHAR_LENGTH)

    class Meta:
        verbose_name = _(u'Статус заявки')
        verbose_name_plural = _(u'Статусы заявок')

    def __unicode__(self):
        return self.status_name


#Dynamic Settings
class DynamicSettings(models.Model):
    INT_FIELD_VALUE = 0
    CHAR_FIELD_VALUE = 1
    TIME_PERIOD_FIELD_VALUE = 2

    code = models.CharField(_(u'Код'), max_length=ModelConstants.MAX_CODE_VARCHAR_LENGTH, primary_key=True,
                            editable=False)
    name = models.CharField(_(u'Параметр'), max_length=ModelConstants.DEFAULT_VARCHAR_LENGTH, editable=False)
    description = models.CharField(max_length=ModelConstants.MAX_VARCHAR_LENGTH, editable=False, null=True)
    field_type = models.IntegerField(_(u'Тип данных'), editable=False, choices=(
        (INT_FIELD_VALUE, _(u'Целочисленный')),
        (CHAR_FIELD_VALUE, _(u'Строковый')),
        (TIME_PERIOD_FIELD_VALUE, _(u'Период времени')))
    )
    value = models.CharField(_(u'Значение'), max_length=ModelConstants.MAX_VARCHAR_LENGTH, null=True)

    class Meta:
        verbose_name = _(u'Настройка')
        verbose_name_plural = _(u'Настройки')

    #"static" variable
    _date_regex = re.compile(r'^(?:(?P<days>\d+)\sdays?,\s)?(?P<hours>\d+):(?P<minutes>\d+):(?P<seconds>\d+)$')

    def get_value(self):
        """Gets the typed value of the setting"""

        def parse_string_to_timedelta(string):
            """Parses the default timedelta string representation back to timedelta object"""
            d = DynamicSettings._date_regex.match(string).groupdict(0)
            return timedelta(**dict(( (key, int(value)) for key, value in d.items() )))

        result = None
        if self.field_type == DynamicSettings.INT_FIELD_VALUE:
            result = int(self.value)
        elif self.field_type == DynamicSettings.TIME_PERIOD_FIELD_VALUE:
            result = parse_string_to_timedelta(self.value)
        elif self.field_type == DynamicSettings.CHAR_FIELD_VALUE:
            result = self.value
        else:
            raise
        return result

    def __unicode__(self):
        return self.name

    class UnknownFieldTypeError(ValueError):
        def __init__(self, type_value, *args, **kwargs):
            self.type_value = type_value
            ValueError.__init__(*args, **kwargs)


#Primary objects
class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True, verbose_name='Учетная запись')
    first_name = models.CharField(_(u'Имя'), max_length=ModelConstants.MAX_NAME_LENGTH)
    last_name = models.CharField(_(u'Фамилия'), max_length=ModelConstants.MAX_NAME_LENGTH)
    middle_name = models.CharField(_(u'Отчество'), max_length=ModelConstants.MAX_NAME_LENGTH)

    first_name_accusative = models.CharField(_(u'Имя (вин.)'), max_length=ModelConstants.MAX_NAME_LENGTH, blank=True,
                                             null=True)
    last_name_accusative = models.CharField(_(u'Фамилия (вин.)'), max_length=ModelConstants.MAX_NAME_LENGTH, blank=True,
                                            null=True)
    middle_name_accusative = models.CharField(_(u'Отчество (вин.)'), max_length=ModelConstants.MAX_NAME_LENGTH,
                                              blank=True, null=True)

    position = models.ForeignKey(Position, verbose_name=_(u'Должность'))
    sign = models.ImageField(_(u'Подпись'), max_length=ModelConstants.DEFAULT_VARCHAR_LENGTH, upload_to='signs',
                             blank=True, null=True)
    email = models.EmailField(_(u'Email'), max_length=ModelConstants.DEFAULT_VARCHAR_LENGTH)
    manager = models.ForeignKey('self', verbose_name=_(u'Руководитель'), blank=True, null=True)

    def get_full_name(self):
        return u"{0} {1} {2}".format(self.last_name, self.first_name, self.middle_name)

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


class Document(models.Model):
    def upload_to(self):
        return 'documents/new'

    def upload_to_signed(self):
        return 'documents/signed'

    date = models.DateField(_(u'Дата договора'))
    active_period = models.IntegerField(_(u'Срок действия'))
    prolongation = models.BooleanField(_(u'Возможность пролонгации'), blank=True, default=False)
    paid_date = models.DateField(_(u'Дата оплаты'))

    contents = models.FileField(_(u'Документ'), upload_to=upload_to)
    contents_signed = models.FileField(_(u'Подписанный документ'), upload_to=upload_to_signed, null=True, blank=True)

    def __unicode__(self):
        return u"{0} {2} {1} {3}".format(_("Документ №"), _(u"от"), self.pk, self.date)

    class Meta:
        verbose_name = _(u"Документ")
        verbose_name_plural = _(u"Документы")


class Request(models.Model):
    name = models.CharField(_(u'Наименование'), max_length=ModelConstants.MAX_NAME_LENGTH)
    comments = models.CharField(_(u'Комментарии'), max_length=ModelConstants.MAX_VARCHAR_LENGTH)
    created = models.DateField(_(u'Дата заведения заявки'), auto_now_add=True)
    accepted = models.DateField(_(u'Дата согласования'), blank=True, null=True)

    city = models.ForeignKey(City, verbose_name=_(u'Город действия'))
    status = models.ForeignKey(RequestStatus, verbose_name=_(u'Статус'))
    document = models.OneToOneField(Document, verbose_name=_(u'Документ'), related_name='document', blank=True, null=True)
    creator = models.ForeignKey(UserProfile, verbose_name=_(u'Инициатор'), related_name='created_by')
    send_on_approval = models.ForeignKey(UserProfile, verbose_name=_(u'Отправить на подпись'))

    class Meta:
        verbose_name = _(u'Заявка')
        verbose_name_plural = _(u'Заявки')
        permissions = (
            ("docapproval.can_create_requests", _(u"Может создавать запросы на утверждение")),
            ("docapproval.can_approve_requests", _(u"Может утверждать документы"))
        )

    def __unicode__(self):
        return u"{0} {2} {1} {3}".format(_(u"Заявка"), _(u"от"), self.name, self.created)
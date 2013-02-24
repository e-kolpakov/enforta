#-*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from global_constants import GlobalConstants
from datetime import timedelta
import re
from django.utils.translation import ugettext as _

#Some "dictionaries" first
class Position(models.Model):
    position_name = models.CharField(u'Должность',max_length=GlobalConstants.MAX_VARCHAR_LENGTH)
    class Meta:
        verbose_name = u'Должность'
        verbose_name_plural = u'Должности'

class City(models.Model):
    city_name = models.CharField(u'Название города', max_length=GlobalConstants.MAX_VARCHAR_LENGTH)
    class Meta:
        verbose_name = u'Город'
        verbose_name_plural = u'Города'

    def __unicode__(self):
        return self.city_name

class RequestStatus(models.Model):
    code = models.CharField(u'Код', max_length=GlobalConstants.MAX_CODE_VARCHAR_LENGTH, primary_key=True,
        editable=False)
    status_name = models.CharField(u'Статус', max_length=GlobalConstants.DEFAULT_VARCHAR_LENGTH)
    class Meta:
        verbose_name = u'Статус заявки'
        verbose_name_plural = u'Статусы заявок'

    def __unicode__(self):
        return self.status_name

#Dynamic Settings
class DynamicSettings(models.Model):
    code = models.CharField(u'Код', max_length=GlobalConstants.MAX_CODE_VARCHAR_LENGTH, primary_key=True,
        editable=False)
    name = models.CharField(u'Параметр',max_length=GlobalConstants.DEFAULT_VARCHAR_LENGTH, editable=False)
    type = models.IntegerField(u'Тип данных', editable=False,
        choices=(
            (GlobalConstants.INT_FIELD_VALUE, u'Целочисленный'),
            (GlobalConstants.CHAR_FIELD_VALUE, u'Строковый'),
            (GlobalConstants.TIME_PERIOD_FIELD_VALUE, u'Период времени')
        )
    )
    value = models.CharField(u'Значение', max_length=GlobalConstants.MAX_VARCHAR_LENGTH, null=True)

    class Meta:
        verbose_name = u'Настройка'
        verbose_name_plural = u'Настройки'

    #"static" variable
    _date_regex = re.compile(r'^(?:(?P<days>\d+)\sdays?,\s)?(?P<hours>\d+):(?P<minutes>\d+):(?P<seconds>\d+)$')

    def get_value(self):
        """Gets the typed value of the setting"""
        def parse_string_to_timedelta(string):
            """Parses the default timedelta string representation back to timedelta object"""
            d = DynamicSettings._date_regex.match(string).groupdict(0)
            return timedelta(**dict(( (key, int(value)) for key, value in d.items() )))

        result = None
        if self.type == GlobalConstants.INT_FIELD_VALUE:
            result = int(self.value)
        elif self.type == GlobalConstants.TIME_PERIOD_FIELD_VALUE:
            result = parse_string_to_timedelta(self.value)
        else:
            result = self.value
        return result

    def __unicode__(self):
        return self.name



#Primary objects
class UserData(models.Model):
    user = models.OneToOneField(User, primary_key=True, verbose_name='Логин')
    first_name = models.CharField(u'Имя', max_length=GlobalConstants.MAX_NAME_LENGTH)
    last_name = models.CharField(u'Фамилия', max_length=GlobalConstants.MAX_NAME_LENGTH)
    middle_name = models.CharField(u'Отчество', max_length=GlobalConstants.MAX_NAME_LENGTH)

    first_name_accusative = models.CharField(u'Имя (вин.)', max_length=GlobalConstants.MAX_NAME_LENGTH, blank=True, null=True)
    last_name_accusative = models.CharField(u'Фамилия (вин.)', max_length=GlobalConstants.MAX_NAME_LENGTH, blank=True, null=True)
    middle_name_accusative = models.CharField(u'Отчество (вин.)', max_length=GlobalConstants.MAX_NAME_LENGTH, blank=True, null=True)

    position = models.ForeignKey(Position, verbose_name=u'Должность')
    sign = models.ImageField(u'Подпись', max_length=GlobalConstants.DEFAULT_VARCHAR_LENGTH, upload_to='signs')
    email = models.EmailField(u'Email', max_length=GlobalConstants.DEFAULT_VARCHAR_LENGTH)
    manager = models.ForeignKey('self')

    def get_full_name(self):
        return "{0} {1} {2}".format(self.last_name, self.first_name, self.middle_name)

    def get_full_name_accusative(self):
        #gets accusative full name, falls back to using subjective case if accusatives is empty
        eff_first_accusative = self.first_name_accusative if self.first_name_accusative else self.first_name
        eff_last_accusative = self.last_name_accusative if self.last_name_accusative else self.last_name
        eff_middle_accusative = self.middle_name_accusative if self.middle_name_accusative else self.middle_name
        return "{0} {1} {2}".format(eff_last_accusative, eff_first_accusative, eff_middle_accusative)

    def __unicode__(self):
        return "{0} {1}".format(_("Пользователь"), self.get_full_name())

    class Meta:
        verbose_name = u'Пользовательские данные'
        verbose_name_plural = u'Пользовательские данные'

class Document(models.Model):
    def upload_to(self):
        return 'documents/new'

    def upload_to_signed(self):
        return 'documents/signed'

    date = models.DateField(u'Дата договора')
    active_period = models.IntegerField(u'Срок действия')
    prolongation = models.BooleanField(u'Возможность рролонгации', blank=True, default=False)
    paid_date = models.DateField(u'Дата оплаты')

    contents = models.FileField(u'Документ', upload_to=upload_to)
    contents_signed = models.FileField(u'Подписанный документ', upload_to=upload_to_signed, null=True, blank=True)

    def __unicode__(self):
        return "{0} {2} {1} {3}".format(_("Документ №"), _("от"), self.pk, self.date)

class Request(models.Model):
    name = models.CharField(u'Наименование', max_length=GlobalConstants.MAX_NAME_LENGTH)
    comments = models.CharField(u'Комментарии', max_length=GlobalConstants.MAX_VARCHAR_LENGTH)
    created = models.DateField(u'Дата заведения заявки', auto_now_add=True)
    accepted = models.DateField(u'Дата согласования', blank=True, default=False)

    city = models.ForeignKey(City, verbose_name=u'Город действия')
    status = models.ForeignKey(RequestStatus, verbose_name=u'Статус')
    document = models.OneToOneField(Document, related_name='document')
    creator = models.ForeignKey(UserData, verbose_name=u'Инициатор', related_name='created_by')
    send_on_approval = models.ForeignKey(UserData, verbose_name=u'Отправить на подпись')

    class Meta:
        verbose_name = u'Заявка'
        verbose_name_plural = u'Заявки'

    def __unicode__(self):
        return "{0} {2} {1} {3}".format(_("Заявка"), _("от"),self.name, self.created)
#-*- coding: utf-8 -*-
import os

from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from .common import City, Position, ModelConstants, Permissions
from DocApproval.url_naming.names import Profile as ProfileUrls


class UserProfile(models.Model):
    def upload_to(self, filename):
        fname, fext = os.path.splitext(filename)
        return u'signs/{0}/sign{1}'.format(self.pk, fext)

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

    @property
    def short_name(self):
        return u"{0} {1}".format(self.last_name, self.first_name)

    @property
    def full_name(self):
        return u"{0} {1} {2}".format(self.last_name, self.first_name, self.middle_name)

    @property
    def full_name_accusative(self):
        #gets accusative full name, falls back to using subjective case if accusatives is empty
        eff_first_accusative = self.first_name_accusative if self.first_name_accusative else self.first_name
        eff_last_accusative = self.last_name_accusative if self.last_name_accusative else self.last_name
        eff_middle_accusative = self.middle_name_accusative if self.middle_name_accusative else self.middle_name
        return "{0} {1} {2}".format(eff_last_accusative, eff_first_accusative, eff_middle_accusative)

    def __unicode__(self):
        return u"{0} ({1})".format(self.full_name, self.position)

    class Meta:
        app_label = "DocApproval"
        verbose_name = _(u'Пользовательские данные')
        verbose_name_plural = _(u'Пользовательские данные')
        permissions = (
            (Permissions.UserProfile.CAN_CHANGE_POSITION, _(u"Может изменять должность")),
            (Permissions.UserProfile.CAN_CHANGE_MANAGER, _(u"Может изменять руководителя")),

            (Permissions.UserProfile.CAN_CHANGE_ANY_POSITION, _(u"Может изменять должность других пользователей")),
            (Permissions.UserProfile.CAN_CHANGE_ANY_MANAGER, _(u"Может изменять руководителя других пользователей")),
        )

    @classmethod
    def get_users_in_group(cls, group_name):
        return cls.objects.filter(user__groups__name=group_name)


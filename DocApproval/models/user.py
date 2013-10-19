#-*- coding: utf-8 -*-
import os
import datetime

from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User
from django.db.models.query_utils import Q
from django.utils.translation import ugettext as _

from .common import City, Position, ModelConstants, Permissions
from DocApproval.url_naming.names import Profile as ProfileUrls


class CanNotImpersonateUser(Exception):
    def __init__(self, profile, impersonated_profile):
        self.message = _(u"Пользователь {0} не имеет права на осуществление действий от имени {1}"). \
            format(profile, impersonated_profile)


class UserManager(models.Manager):
    def get_users_in_group(self, group_name):
        return self.filter(user__groups__name=group_name)

    def get_active_users(self):
        return self.filter(user__is_active=True)


class UserProfile(models.Model):
    objects = UserManager()

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

    # not a db field
    _replacements = None

    def get_absolute_url(self):
        return reverse(ProfileUrls.PROFILE, kwargs={'pk': self.pk})

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
        return u"{0} {1} {2}".format(eff_last_accusative, eff_first_accusative, eff_middle_accusative)

    @property
    def active_replacements(self):
        if not self._replacements:
            now = datetime.datetime.now()
            qs = self.replacing.filter(
                Q(replacement_end__isnull=True) | Q(replacement_end__gte=now),
                replacement_start__lte=now
            )
            self._replacements = [replacement for replacement in qs.select_related('replaced_user__user')]
        return self._replacements

    @property
    def effective_profiles(self):
        """
        Returns set of effective profiles for current profile.
        This profile is always active.
        Other users' profiles are added if there is an active temporary replacement other=>this
        """
        return {self} | set(repl.replaced_user for repl in self.active_replacements)

    @property
    def effective_accounts(self):
        """
        Returns set of effective accounts for current profile.
        This user account is always active.
        Other users' accounts are added if there is an active temporary replacement other=>this
        """
        return {self.user} | set(repl.replaced_user.user for repl in self.active_replacements)

    def can_impersonate(self, other_profile):
        return other_profile in self.effective_profiles

    def can_approve(self, request):
        current_approvers = request.get_current_approvers()
        replacements = [replacement.replaced_user for replacement in self.active_replacements]
        check_against = {self} | set(replacements)
        return any(user in current_approvers for user in check_against)


class TemporaryUserImpersonation(models.Model):
    replaced_user = models.ForeignKey(UserProfile, verbose_name=_(u"Замещаемый"), related_name='replaced_by')
    new_user = models.ForeignKey(UserProfile, verbose_name=_(u"Замещающий"), related_name='replacing')
    replacement_start = models.DateField(verbose_name=_(u"Начало периода"))
    replacement_end = models.DateField(verbose_name=_(u"Конец периода"), null=True, blank=True)

    class Meta:
        app_label = 'DocApproval'
        verbose_name = _(u'Временное замещение')
        verbose_name_plural = _(u'Временные замещения')
        permissions = (
            (Permissions.TemplateUserReplacements.CAN_MANAGE_REPLACEMENTS,
             _(u"Может управлять временным замещением пользователей")),
        )

    def __unicode__(self):
        return _(u"{0} замещен {1} {2}").format(self.replaced_user, self.new_user, self.date_period())

    def date_period(self):
        eff_end_date = self.replacement_end if self.replacement_end else _(u"неопределённый срок")
        return _(u"с {0} по {1}").format(self.replacement_start, eff_end_date)

    date_period.short_description = _(u"Период")
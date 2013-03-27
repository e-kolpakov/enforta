# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.forms import (UserCreationForm, UserChangeForm)
from django.utils.translation import ugettext as _

from models import (Position, UserProfile)
import widgets


class PositionForm(forms.ModelForm):
    class Meta:
        model = Position


class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField()
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)
    qweqwe = forms.DateField(widget=widgets.DatepickerWidget)


class CreateUserForm(UserCreationForm):
    class Meta:
        model = UserProfile


class ChangeUserForm(UserChangeForm):
    middle_name = forms.CharField(label=_(u"Отчество"), widget=forms.TextInput)

    first_name_accusative = forms.CharField(label=_(u"Имя (вин.)"), widget=forms.TextInput)
    last_name_accusative = forms.CharField(label=_(u"Фамилия (вин.)"), widget=forms.TextInput)
    middle_name_accusative = forms.CharField(label=_(u"Отчество (вин.)"), widget=forms.TextInput)

    class Meta:
        model = UserProfile
        add_fields = ('middle_name', 'first_name_accusative', 'last_name_accusative', 'middle_name_accusative')
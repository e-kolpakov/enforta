#-*- coding: utf-8 -*-

from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth.models import Permission
from django.contrib.auth.forms import UserChangeForm
from django.utils.translation import ugettext as _

from models import (UserProfile, Request, Contract, Permissions)
from widgets import DatePickerWidget


class CreateRequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ('name', 'city', 'send_on_approval', 'comments')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'span4'}),
            'city': forms.Select(attrs={'class': 'span4'}),
            'send_on_approval': forms.Select(attrs={'class': 'span4'}),
            'comments': forms.Textarea(attrs={'rows': 10, 'class': 'span4'}),
        }


class CreateContractForm(forms.ModelForm):
    #TODO: use bootstrap's appended buttons to provide sets of common active periods, e.g. 1 year, 6 month, etc.

    class Meta:
        model = Contract
        fields = ('date', 'prolongation', 'active_period', 'document')
        widgets = {
            'date': DatePickerWidget(attrs={'class': 'span4'})
        }


class UpdateRequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ('name', 'city', 'status', 'send_on_approval', 'comments')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'span4'}),
            'city': forms.Select(attrs={'class': 'span4'}),
            'status': forms.Select(attrs={'class': 'span4'}),
            'send_on_approval': forms.Select(attrs={'class': 'span4'}),
            'comments': forms.Textarea(attrs={'rows': 10, 'class': 'span4'}),
        }


class UpdateContractForm(forms.ModelForm):
    class Meta:
        model = Contract
        fields = ('date', 'prolongation', 'active_period', 'document')
        widgets = {
            'date': DatePickerWidget(attrs={'class': 'span4'})
        }


class UserProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self._process_permission('position', True)
        self._process_permission('manager', True)

    def _process_permission(self, field, permitted):
        if not permitted:
            self.fields.pop(field)

    class Meta:
        model = UserProfile
        fields = ['last_name', 'first_name', 'middle_name',
                  'email', 'sign', 'position', 'manager',
                  'last_name_accusative', 'first_name_accusative', 'middle_name_accusative']


class AdminCustomizedUserForm(UserChangeForm):
    user_permissions = forms.ModelMultipleChoiceField(
        Permission.objects.filter(codename__startswith=Permissions.PREFIX),
        widget=FilteredSelectMultiple(_('permissions'), False))

    def __init__(self, *args, **kwargs):
        super(AdminCustomizedUserForm, self).__init__(*args, **kwargs)
        self.fields['user_permissions'].label = unicode.capitalize(_("user permissions"))


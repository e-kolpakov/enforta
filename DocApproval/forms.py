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
            'comments': forms.Textarea(attrs={'rows': 10}),
        }


class CreateContractForm(forms.ModelForm):
    #TODO: use bootstrap's appended buttons to provide sets of common active periods, e.g. 1 year, 6 month, etc.
    class Meta:
        model = Contract
        fields = ('date', 'prolongation', 'active_period', 'document')
        widgets = {
            'date': DatePickerWidget()
        }


class UpdateRequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ('name', 'city', 'status', 'send_on_approval', 'comments')
        widgets = {
            # 'city': forms.Select(attrs={'readonly': 'readonly', 'disabled': 'disabled'}),
            'comments': forms.Textarea(attrs={'rows': 10}),
        }
    #
    # def clean_city(self):
    #     new_city = self.cleaned_data['city']
    #     if self.instance and self.instance.city != new_city:
    #         raise ValidationError(RequestMessages.CANT_CHANGE_CITY)
    #     return self.instance.city


class UpdateContractForm(forms.ModelForm):
    class Meta:
        model = Contract
        fields = ('date', 'prolongation', 'active_period', 'document')
        widgets = {
            'date': DatePickerWidget()
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
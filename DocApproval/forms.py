from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth.models import Permission
from django.contrib.auth.forms import UserChangeForm
from django.utils.translation import ugettext as _

from models import (UserProfile, Request, Permissions)


class CreateRequestForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CreateRequestForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder = ['name', 'city', 'send_on_approval', 'comments']

    class Meta:
        model = Request
        exclude = ('document', 'status', 'creator', 'created', 'accepted')
        widgets = {
            'comments': forms.Textarea(attrs={'rows': 10}),
        }


class UserProfileForm(forms.ModelForm):
    def __init__(self, can_change_position=False, can_change_manager=False, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder = [
            'last_name', 'first_name', 'middle_name',
            'email', 'sign',
            'last_name_accusative', 'first_name_accusative', 'middle_name_accusative',
        ]
        self._process_permission('position', can_change_position)
        self._process_permission('manager', can_change_manager)

    def _process_permission(self, field, permitted):
        if permitted:
            self.fields.keyOrder.append(field)
        else:
            self.Meta.exclude.append(field)

    class Meta:
        model = UserProfile
        exclude = []

class AdminCustomizedUserForm(UserChangeForm):
    user_permissions = forms.ModelMultipleChoiceField(
        Permission.objects.filter(codename__startswith=Permissions.PREFIX),
        widget=FilteredSelectMultiple(_('permissions'), False))

    def __init__(self, *args, **kwargs):
        super(AdminCustomizedUserForm, self).__init__(*args, **kwargs)
        self.fields['user_permissions'].label = unicode.capitalize(_("user permissions"))
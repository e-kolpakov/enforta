from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth.models import Permission
from django.contrib.auth.forms import UserChangeForm
from django.utils.translation import ugettext as _

from models import *


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


class AdminCustomizedUserForm(UserChangeForm):
    user_permissions = forms.ModelMultipleChoiceField(
        Permission.objects.filter(codename__startswith=Permissions.PREFIX),
        widget=FilteredSelectMultiple(_('permissions'), False))

    def __init__(self, *args, **kwargs):
        super(AdminCustomizedUserForm, self).__init__(*args, **kwargs)
        self.fields['user_permissions'].label = unicode.capitalize(_("user permissions"))
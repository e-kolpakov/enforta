#-*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
import reversion
from django.utils.translation import ugettext as _

from models import *
from forms import (CreateUserForm, ChangeUserForm)


class CustomizedUserAdmin(UserAdmin):
    add_form = CreateUserForm
    form = ChangeUserForm
    fieldsets = (
        (None, {'fields': ('username', 'password', 'email', 'is_active')}),
        (_('Personal info'),
         {'fields': (
             'first_name', 'last_name', 'middle_name',
             'first_name_accusative', 'last_name_accusative', 'middle_name_accusative'
         )}),
        (_('Permissions'), {'fields': ('groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )


# "dictionaries"
class PositionAdmin(admin.ModelAdmin):
    pass


class CityAdmin(admin.ModelAdmin):
    pass


class RequestStatusAdmin(admin.ModelAdmin):
    fields = ("status_name",)
    readonly_fields = ("code",) #code is not editable anyway, it's included for the sake of completeness
    actions = None

    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request, obj=None):
        return False


#Dynamic Settings
class DynamicSettingsAdmin(admin.ModelAdmin):
    fields = ("code", "name", "field_type", "value", "description")
    #these are not editable anyway, it's included for the sake of completeness
    readonly_fields = ("code","name", "field_type", "description")
    list_display = ("name", "value", "description")
    actions = None

    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request, obj=None):
        return False


#Primary data objects
class RequestAdmin(reversion.VersionAdmin):
    history_latest_first = True
    ignore_duplicate_revisions = True

admin.site.unregister(get_user_model())
admin.site.register(get_user_model(), CustomizedUserAdmin)

admin.site.register(City, CityAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(RequestStatus, RequestStatusAdmin)

admin.site.register(DynamicSettings, DynamicSettingsAdmin)

admin.site.register(Request, RequestAdmin)
#-*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
import django.contrib.auth.models as auth_models
from models import *
import reversion
from django.utils.translation import ugettext as _
# "dictionaries"
class CustomizedUserAdmin(UserAdmin):
    fieldsets = (
        ( None, {'fields': ('username', 'password', 'is_active')}),
        (_('Permissions'), {'fields': ('groups',)})
    )

class UserProfileAdmin(admin.ModelAdmin):
    pass

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

admin.site.unregister(auth_models.User)
admin.site.register(auth_models.User, CustomizedUserAdmin)

admin.site.register(City, CityAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(RequestStatus, RequestStatusAdmin)

admin.site.register(DynamicSettings, DynamicSettingsAdmin)

admin.site.register(Request, RequestAdmin)
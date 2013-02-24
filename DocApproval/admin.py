#-*- coding: utf-8 -*-
from django.contrib import admin
from models import *
import reversion

#"dictionaries"
class UserDataAdmin(admin.ModelAdmin):
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
    fields = ("code", "name", "type", "value")
    readonly_fields = ("code","name", "type") #these are not editable anyway, it's included for the sake of completeness
    list_display = ("name", "value")
    actions = None

    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request, obj=None):
        return False

#Primary data objects
class RequestAdmin(reversion.VersionAdmin):
    history_latest_first = True
    ignore_duplicate_revisions = True

admin.site.register(City, CityAdmin)
admin.site.register(UserData, UserDataAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(RequestStatus, RequestStatusAdmin)

admin.site.register(DynamicSettings, DynamicSettingsAdmin)

admin.site.register(Request, RequestAdmin)
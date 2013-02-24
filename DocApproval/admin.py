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
    pass

#Dynamic Settings
class DynamicSettingsAdmin(admin.ModelAdmin):
    pass

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
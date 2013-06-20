#-*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
import django.contrib.auth.models as auth_models
import reversion
from django.utils.translation import ugettext as _

from models import *
from forms import AdminCustomizedUserForm


class NonDeleteableEntityAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super(NonDeleteableEntityAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


class CustomizedUserAdmin(NonDeleteableEntityAdmin, UserAdmin):
    form = AdminCustomizedUserForm
    fieldsets = (
        ( None, {'fields': ('username', 'password', 'is_active')}),
        (_('Permissions'), {'fields': ('groups', 'user_permissions')})
    )


class UserProfileAdmin(NonDeleteableEntityAdmin):
    pass


class PositionAdmin(admin.ModelAdmin):
    pass


class CityAdmin(admin.ModelAdmin):
    pass


class TemporaryUserReplacementAdmin(admin.ModelAdmin):
    list_display = ('replaced_user', 'new_user', 'date_period')
    search_fields = (
        '^replaced_user__first_name', '^replaced_user__middle_name', '^replaced_user__last_name',
        '^new_user__first_name', '^new_user__middle_name', '^new_user__last_name',
        'replacement_start', 'replacement_end'
    )


class RequestStatusAdmin(NonDeleteableEntityAdmin):
    fields = ("name",)
    readonly_fields = ("code",) #code is not editable anyway, it's included for the sake of completeness

    def has_add_permission(self, request, obj=None):
        return False


#Primary data objects
class RequestAdmin(reversion.VersionAdmin):
    history_latest_first = True
    ignore_duplicate_revisions = True


class ContractAdmin(reversion.VersionAdmin):
    history_latest_first = True
    ignore_duplicate_revisions = True


admin.site.unregister(auth_models.User)
admin.site.register(auth_models.User, CustomizedUserAdmin)

admin.site.register(City, CityAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(TemporaryUserReplacement, TemporaryUserReplacementAdmin)
admin.site.register(RequestStatus, RequestStatusAdmin)

admin.site.register(Request, RequestAdmin)
admin.site.register(Contract, ContractAdmin)
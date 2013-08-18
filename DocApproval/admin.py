#-*- coding: utf-8 -*-
import reversion

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.utils.translation import ugettext as _
import django.contrib.auth.models as auth_models

from DocApproval.models import *
from DocApproval.forms import AdminCustomizedUserForm, AdminCustomizedGroupForm


class NonDeleteableEntityAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super(NonDeleteableEntityAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


class CustomizedUserAdmin(UserAdmin):
    form = AdminCustomizedUserForm
    fieldsets = (
        ( None, {'fields': ('username', 'password', 'is_active')}),
        (_('Permissions'), {'fields': ('groups', 'user_permissions')})
    )

    class Media:
        css = {
            'all': ('css/admin_overrides_bundle.css',)
        }


class CustomizedGroupAdmin(GroupAdmin):
    form = AdminCustomizedGroupForm

    class Media:
        css = {
            'all': ('css/admin_overrides_bundle.css',)
        }


class UserProfileAdmin(admin.ModelAdmin):
    pass


class PositionAdmin(admin.ModelAdmin):
    pass


class CityAdmin(admin.ModelAdmin):
    pass


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'responsible_user')


class TemporaryUserImpersonationAdmin(admin.ModelAdmin):
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
admin.site.unregister(auth_models.Group)
admin.site.register(auth_models.User, CustomizedUserAdmin)
admin.site.register(auth_models.Group, CustomizedGroupAdmin)

admin.site.register(City, CityAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(Department, DepartmentAdmin)

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(TemporaryUserImpersonation, TemporaryUserImpersonationAdmin)
admin.site.register(RequestStatus, RequestStatusAdmin)

admin.site.register(Request, RequestAdmin)
admin.site.register(Contract, ContractAdmin)
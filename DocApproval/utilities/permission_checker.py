#taken from http://code.activestate.com/recipes/52549-curry-associating-parameters-with-a-function/
from DocApproval.models import Permissions


class curry:
    def __init__(self, fun, *args, **kwargs):
        self.fun = fun
        self.pending = args[:]
        self.kwargs = kwargs.copy()

    def __call__(self, *args, **kwargs):
        if kwargs and self.kwargs:
            kw = self.kwargs.copy()
            kw.update(kwargs)
        else:
            kw = kwargs or self.kwargs

        return self.fun(*(self.pending + args), **kw)


class PermissionChecker(object):
    def __init__(self, user):
        self.user = user

    def check_object_permission(self, user, permission, obj):
        return user.has_perm(permission, obj)

    def check_entity_permission(self, user, permission):
        return user.has_perm(permission)

    def check_permission(self, permission, obj=None):
        eff_perm = Permissions._(permission)
        if obj:
            resolver = curry(self.check_object_permission, permission=eff_perm, obj=obj)
        else:
            resolver = curry(self.check_entity_permission, permission=eff_perm)

        replaces_users = [replacement.replaced_user.user for replacement in self.user.profile.active_replacements]

        check_permissions_for = {self.user} | set(replaces_users)
        return any(resolver(user) for user in check_permissions_for)



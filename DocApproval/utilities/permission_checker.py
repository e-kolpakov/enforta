import types
import logging
from functools import partial, wraps

from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.core.exceptions import PermissionDenied
from django.db.models import Model, get_model
from django.db.models.base import ModelBase
from django.db.models.query import QuerySet
from django.http.response import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template.base import TemplateDoesNotExist
from django.template.context import RequestContext
from django.utils.http import urlquote
from guardian.compat import basestring

from guardian.exceptions import GuardianError
from guardian.conf import settings as guardian_settings

from DocApproval.utilities.utility import wrap_permission

# Fixme: All this is one big hack. Need to rethink that impersonation thing.


class PermissionChecker(object):
    def __init__(self, user):
        self.user = user

    def _get_permissions(self, permissions):
        if permissions is None:
            return []
        if isinstance(permissions, types.StringTypes):
            return [wrap_permission(permissions)]
        else:
            try:
                iterable = iter(permissions)
            except TypeError, te:
                logger = logging.getLogger(__name__)
                logger.exception(te)
                raise
            return [wrap_permission(perm) for perm in permissions]

    def check_object_permissions(self, user, permissions, instance):
        check = lambda permission: user.has_perm(permission, instance)
        return any(check(perm) for perm in permissions)

    def check_entity_permissions(self, user, permissions):
        check = lambda permission: user.has_perm(permission)
        return any(check(perm) for perm in permissions)

    def check_permission(self, instance_permissions=None, class_permissions=None, instance=None):
        instance_resolver = partial(
            self.check_object_permissions,
            permissions=self._get_permissions(instance_permissions),
            instance=instance)
        class_resolver = partial(
            self.check_entity_permissions,
            permissions=self._get_permissions(class_permissions))

        return (any(instance_resolver(user) for user in self.user.profile.effective_accounts) |
                any(class_resolver(user) for user in self.user.profile.effective_accounts))


# Fixme: mostly copy-pasted guardian internals.
def impersonated_permission_required(instance_permissions=None, class_permissions=None, lookup_variables=None,
                                     **kwargs):
    login_url = kwargs.pop('login_url', settings.LOGIN_URL)
    redirect_field_name = kwargs.pop('redirect_field_name', REDIRECT_FIELD_NAME)
    return_403 = kwargs.pop('return_403', False)

    def get_obj(*args, **kwargs):
        if lookup_variables:
            model, lookups = lookup_variables[0], lookup_variables[1:]
            # Parse model
            if isinstance(model, basestring):
                splitted = model.split('.')
                if len(splitted) != 2:
                    raise GuardianError("If model should be looked up from "
                                        "string it needs format: 'app_label.ModelClass'")
                model = get_model(*splitted)
            elif issubclass(model.__class__, (Model, ModelBase, QuerySet)):
                pass
            else:
                raise GuardianError("First lookup argument must always be "
                                    "a model, string pointing at app/model or queryset. "
                                    "Given: %s (type: %s)" % (model, type(model)))
                # Parse lookups
            if len(lookups) % 2 != 0:
                raise GuardianError("Lookup variables must be provided as pairs of lookup_string and view_arg")
            lookup_dict = {}
            for lookup, view_arg in zip(lookups[::2], lookups[1::2]):
                if view_arg not in kwargs:
                    raise GuardianError("Argument %s was not passed into view function" % view_arg)
                lookup_dict[lookup] = kwargs[view_arg]
            return get_object_or_404(model, **lookup_dict)
        else:
            return None

    def process_missing_permission(request):
        if return_403:
            if guardian_settings.RENDER_403:
                try:
                    response = render_to_response(guardian_settings.TEMPLATE_403, {}, RequestContext(request))
                    response.status_code = 403
                    return response
                except TemplateDoesNotExist as e:
                    if settings.DEBUG:
                        raise e
            elif guardian_settings.RAISE_403:
                raise PermissionDenied
            return HttpResponseForbidden()
        else:
            path = urlquote(request.get_full_path())
            tup = login_url, redirect_field_name, path
            return HttpResponseRedirect("%s?%s=%s" % tup)

    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            checker = PermissionChecker(request.user)
            obj = get_obj(*args, **kwargs)
            has_permission = checker.check_permission(
                instance_permissions=instance_permissions,
                class_permissions=class_permissions,
                instance=obj)

            if not has_permission:
                return process_missing_permission(request)

            return view_func(request, *args, **kwargs)

        return wraps(view_func)(_wrapped_view)

    return decorator
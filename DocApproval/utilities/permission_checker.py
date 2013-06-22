from functools import partial, wraps
from itertools import groupby

from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME, get_user_model
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.db.models import Model, get_model
from django.db.models.base import ModelBase
from django.db.models.query import QuerySet
from django.http.response import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response, _get_queryset
from django.template.base import TemplateDoesNotExist
from django.template.context import RequestContext
from django.utils.http import urlquote
from guardian.compat import basestring

from guardian.exceptions import GuardianError, MixedContentTypeError, WrongAppError
from guardian.conf import settings as guardian_settings
from guardian.utils import get_user_obj_perms_model, get_group_obj_perms_model

from DocApproval.models.common import Permissions

# Fixme: All this is one big hack. Need to rethink that impersonation thing.

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
            resolver = partial(self.check_object_permission, permission=eff_perm, obj=obj)
        else:
            resolver = partial(self.check_entity_permission, permission=eff_perm)

        return any(resolver(user) for user in self.user.profile.effective_accounts)


# Fixme: mostly copy-pasted guardian internals.
def impersonated_permission_required(perm, lookup_variables=None, **kwargs):
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
            has_permission = checker.check_permission(perm, obj)

            if not has_permission:
                return process_missing_permission(request)

            return view_func(request, *args, **kwargs)

        return wraps(view_func)(_wrapped_view)

    return decorator

# FIXME:
# Copypasted from guardian source code with minor alteration to allow for multiple users.
# Not all paths are tested, and it's a dirty hack anyway.
def get_objects_for_users(users, perms, klass=None, use_groups=True, any_perm=False):
    """
    Returns queryset of objects for which any of given ``users`` has *all*
    permissions present at ``perms``.

    :param user: ``User`` instance for which objects would be returned
    :param perms: single permission string, or sequence of permission strings
      which should be checked.
      If ``klass`` parameter is not given, those should be full permission
      names rather than only codenames (i.e. ``auth.change_user``). If more than
      one permission is present within sequence, their content type **must** be
      the same or ``MixedContentTypeError`` exception would be raised.
    :param klass: may be a Model, Manager or QuerySet object. If not given
      this parameter would be computed based on given ``params``.
    :param use_groups: if ``False``, wouldn't check user's groups object
      permissions. Default is ``True``.
    :param any_perm: if True, any of permission in sequence is accepted

    :raises MixedContentTypeError: when computed content type for ``perms``
      and/or ``klass`` clashes.
    :raises WrongAppError: if cannot compute app label for given ``perms``/
      ``klass``.

    Example::

        >>> from guardian.shortcuts import get_objects_for_user
        >>> joe = User.objects.get(username='joe')
        >>> get_objects_for_user(joe, 'auth.change_group')
        []
        >>> from guardian.shortcuts import assign_perm
        >>> group = Group.objects.create('some group')
        >>> assign_perm('auth.change_group', joe, group)
        >>> get_objects_for_user(joe, 'auth.change_group')
        [<Group some group>]

    The permission string can also be an iterable. Continuing with the previous example:

        >>> get_objects_for_user(joe, ['auth.change_group', 'auth.delete_group'])
        []
        >>> get_objects_for_user(joe, ['auth.change_group', 'auth.delete_group'], any_perm=True)
        [<Group some group>]
        >>> assign_perm('auth.delete_group', joe, group)
        >>> get_objects_for_user(joe, ['auth.change_group', 'auth.delete_group'])
        [<Group some group>]

    """
    if isinstance(perms, basestring):
        perms = [perms]
    ctype = None
    app_label = None
    codenames = set()

    # Compute codenames set and ctype if possible
    for perm in perms:
        if '.' in perm:
            new_app_label, codename = perm.split('.', 1)
            if app_label is not None and app_label != new_app_label:
                raise MixedContentTypeError("Given perms must have same app "
                                            "label (%s != %s)" % (app_label, new_app_label))
            else:
                app_label = new_app_label
        else:
            codename = perm
        codenames.add(codename)
        if app_label is not None:
            new_ctype = ContentType.objects.get(app_label=app_label,
                                                permission__codename=codename)
            if ctype is not None and ctype != new_ctype:
                raise MixedContentTypeError("ContentType was once computed "
                                            "to be %s and another one %s" % (ctype, new_ctype))
            else:
                ctype = new_ctype

    # Compute queryset and ctype if still missing
    if ctype is None and klass is None:
        raise WrongAppError("Cannot determine content type")
    elif ctype is None and klass is not None:
        queryset = _get_queryset(klass)
        ctype = ContentType.objects.get_for_model(queryset.model)
    elif ctype is not None and klass is None:
        queryset = _get_queryset(ctype.model_class())
    else:
        queryset = _get_queryset(klass)
        if ctype.model_class() != queryset.model:
            raise MixedContentTypeError("Content type for given perms and "
                                        "klass differs")

    # At this point, we should have both ctype and queryset and they should
    # match which means: ctype.model_class() == queryset.model
    # we should also have ``codenames`` list

    # First check if any user is superuser and if so, return queryset immediately
    if any(usr.is_superuser for usr in users):
        return queryset

    # Now we should extract list of pk values for which we would filter queryset
    user_model = get_user_obj_perms_model(queryset.model)
    user_obj_perms_queryset = (user_model.objects
                               .filter(user__in=users)
                               .filter(permission__content_type=ctype)
                               .filter(permission__codename__in=codenames))

    if user_model.objects.is_generic():
        fields = ['object_pk', 'permission__codename']
    else:
        fields = ['content_object__pk', 'permission__codename']
    user_obj_perms = user_obj_perms_queryset.values_list(*fields)
    data = list(user_obj_perms)
    if use_groups:
        group_model = get_group_obj_perms_model(queryset.model)
        group_filters = {
            'permission__content_type': ctype,
            'permission__codename__in': codenames,
            'group__%s__in' % get_user_model()._meta.module_name: users,
        }
        groups_obj_perms_queryset = group_model.objects.filter(**group_filters)
        if group_model.objects.is_generic():
            fields = ['object_pk', 'permission__codename']
        else:
            fields = ['content_object__pk', 'permission__codename']
        groups_obj_perms = groups_obj_perms_queryset.values_list(*fields)
        data += list(groups_obj_perms)
    keyfunc = lambda t: t[0] # sorting/grouping by pk (first in result tuple)
    data = sorted(data, key=keyfunc)
    pk_list = []
    for pk, group in groupby(data, keyfunc):
        obj_codenames = set((e[1] for e in group))
        if any_perm or codenames.issubset(obj_codenames):
            pk_list.append(pk)

    objects = queryset.filter(pk__in=pk_list)
    return objects
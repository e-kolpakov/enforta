import logging

from django.views.generic import ( DetailView)
from django.shortcuts import (render )
from django.core.exceptions import ObjectDoesNotExist

from ..models import (UserProfile, Permissions)


class UserProfileView(DetailView):
    template_name = "profile/view.html"

    def get(self, request, *args, **kwargs):
        user_id = kwargs['pk'] if 'pk' in kwargs else request.user.pk
        try:
            user_profile = UserProfile.objects.get(pk=user_id)
        except ObjectDoesNotExist, e:
            logger = logging.getLogger(__name__)
            logger.warning("User profile {0} not found. {1}".format(user_id, e.message))
            user_profile = None

        can_change_position = request.user.has_perm(Permissions.UserProfile.CAN_CHANGE_ANY_POSITION) or (
            request.user.has_perm(Permissions.UserProfile.CAN_CHANGE_POSITION) and user_id == request.user.pk
        )

        can_change_manager = request.user.has_perm(Permissions.UserProfile.CAN_CHANGE_ANY_MANAGER) or (
            request.user.has_perm(Permissions.UserProfile.CAN_CHANGE_MANAGER) and user_id == request.user.pk
        )

        return render(request, self.template_name, {
            'user_profile': user_profile,
            'can_change_position': can_change_position,
            'can_change_manager': can_change_manager
        })
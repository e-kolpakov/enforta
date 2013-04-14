import logging

from django.views.generic import (UpdateView,  DetailView)
from django.shortcuts import (render, )
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages

from ..models import (UserProfile )
from ..messages import ProfileMessages
from ..menu import UserProfileContextMenuManagerExtension
from ..forms import UserProfileForm


class UserProfileDetailsView(DetailView):
    template_name = "profile/details.html"

    def _modify_menu(self, request, profile_id, allow_edit):
        UserProfileContextMenuManagerExtension(request, allow_edit).extend(profile_id)

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get(self.pk_url_kwarg, request.user.pk)
        try:
            user_profile = UserProfile.objects.get(pk=user_id)
            allow_edit = (user_id == request.user.pk) or request.user.is_superuser
            self._modify_menu(request, user_id, allow_edit)
        except ObjectDoesNotExist, e:
            logger = logging.getLogger(__name__)
            logger.warning("User profile {0} not found. {1}".format(user_id, e.message))
            messages.error(request, ProfileMessages.DOES_NOT_EXIST)
            user_profile = None

        exclude_fields = ("user",)



        return render(request, self.template_name, {
            'user_profile': user_profile,
            'exclude_fields': exclude_fields
        })


class UserProfileUpdateView(UpdateView):
    model = UserProfile
    template_name = "profile/update.html"
    form_class = UserProfileForm
    #
    # can_change_position = request.user.has_perm(Permissions.UserProfile.CAN_CHANGE_ANY_POSITION) or (
    #     request.user.has_perm(Permissions.UserProfile.CAN_CHANGE_POSITION) and user_id == request.user.pk
    # )
    #
    # can_change_manager = request.user.has_perm(Permissions.UserProfile.CAN_CHANGE_ANY_MANAGER) or (
    #     request.user.has_perm(Permissions.UserProfile.CAN_CHANGE_MANAGER) and user_id == request.user.pk
    # )
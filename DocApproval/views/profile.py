from django.views.generic import (UpdateView, DetailView)
from django.shortcuts import (render, get_object_or_404)

from ..models import UserProfile
from ..forms import UserProfileForm


class UserProfileDetailsView(DetailView):
    template_name = "profile/details.html"

    def get(self, request, *args, **kwargs):
        user_id = int(kwargs.get(self.pk_url_kwarg, request.user.pk))
        user_profile = get_object_or_404(UserProfile, pk=user_id)

        exclude_fields = ("user",)

        return render(request, self.template_name, {
            'user_profile': user_profile,
            'exclude_fields': exclude_fields
        })


class UserProfileUpdateView(UpdateView):
    model = UserProfile
    template_name = "profile/update.html"
    form_class = UserProfileForm

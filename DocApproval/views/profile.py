import json
import logging

from django.contrib.auth.models import User
from django.http.response import HttpResponse
from django.views.generic import UpdateView, DetailView
from django.shortcuts import render, get_object_or_404
from django.views.generic.base import View

from DocApproval.models import UserProfile, Request
from DocApproval.forms import UserProfileForm
from DocApproval.messages import ProfileMessages


class ImpersonationBackendParameterError(Exception):
    pass


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


class ImpersonationsForRequestView(View):
    _logger = logging.getLogger(__name__)

    def post(self, request, *args, **kwargs):
        try:
            target_profile_pk = request.POST.get('user', None)
            if target_profile_pk:
                target_user = User.objects.get(pk=target_profile_pk)
            else:
                target_user = request.user

            target_request_raw = request.POST.get('request_pk', None)
            if not target_request_raw:
                raise ImpersonationBackendParameterError(ProfileMessages.TARGET_REQUESTS_NOT_SPECIFIED)
            target_request = int(target_request_raw)
            request = Request.objects.get_accessible_requests(target_user).get(pk=target_request)

            impersonations = target_user.profile.effective_profiles & set(request.get_current_approvers())

            data = {
                'success': True,
                'impersonations': {profile.pk: profile.short_name for profile in impersonations}
            }
        except Exception as e:
            self._logger.exception(e)
            data = {
                'success': False,
                'response': None,
                'errors': [unicode(e)]
            }
        return HttpResponse(json.dumps(data), content_type="application/json")
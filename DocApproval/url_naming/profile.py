from django.conf.urls import patterns, url
from names import Profile as profile_names

from ..views import profile

urlpatterns = patterns(
    '',
    # keep this two in sync with /js/services/modal_popup.js impersonations_backend variable
    url(r"^impersonations/request/", profile.ImpersonationsForRequestView.as_view(),
        name=profile_names.CURRENT_USER_IMPERSONATIONS_FOR_REQUEST),
    # url(r"^impersonations/", profile.ImpersonationsView.as_view(), name=profile_names.CURRENT_USER_IMPERSONATIONS),

    url(r"^profile/(?P<pk>\d+)", profile.UserProfileDetailsView.as_view(), name=profile_names.PROFILE),
    url(r"^update/(?P<pk>\d+)", profile.UserProfileUpdateView.as_view(), name=profile_names.UPDATE),
)
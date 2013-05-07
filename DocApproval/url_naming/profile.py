from django.conf.urls import patterns, url
from names import Profile as profile_names

from ..views import profile

urlpatterns = patterns(
    '',
    url(r"^profile/(?P<pk>\d+)", profile.UserProfileDetailsView.as_view(), name=profile_names.PROFILE),
    url(r"^update/(?P<pk>\d+)", profile.UserProfileUpdateView.as_view(), name=profile_names.UPDATE),
)
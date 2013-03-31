from django.conf.urls import patterns, url
from names import Profile as profile_names

from ..views import common

urlpatterns = patterns(
    '',
    url(r"^profile", common.quicktest, name=profile_names.PROFILE),
)
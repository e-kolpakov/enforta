from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.core.urlresolvers import reverse

from DocApproval.url_naming import (authentication, request, profile, approval_route, media)
from DocApproval.url_naming.names import Common as common_urls, Profile as profile_urls
from DocApproval.views import home_page

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/?', include(admin.site.urls)),
    #url(r'^admin/doc/?', include('django.contrib.admindocs.urls')),

    url(r'^/?$', home_page.HomePage.as_view(), name=common_urls.HOME),

    url(r'^accounts/', include(authentication)),
    url(r'^requests/', include(request)),
    url(r'^profile/', include(profile)), # if renamed, update js/services/modal_popup.js impersonations_backend variable
    url(r'^approval/', include(approval_route)),
    url(r'^media/', include(media))
)


def static_urls_processor(request):
    return {'static_urls': {
        'static_root': settings.STATIC_URL,
        'impersonations_backend': reverse(profile_urls.CURRENT_USER_IMPERSONATIONS_FOR_REQUEST)
    }}

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns += staticfiles_urlpatterns()

from django.conf.urls import patterns, include, url
from django.contrib import admin

from DocApproval.url_naming import (authentication, request, profile)
from DocApproval.url_naming.names import Common as common_urls
from DocApproval.views import common

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/?', include(admin.site.urls)),
    #url(r'^admin/doc/?', include('django.contrib.admindocs.urls')),

    url(r'^/?$', common.index, name=common_urls.HOME),
    url(r'^quicktest/$', common.quicktest, name="common.quick_test"),

    url(r'^accounts/', include(authentication)),
    url(r'^requests/', include(request)),
    url(r'^profile/', include(profile))
)

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns += staticfiles_urlpatterns()
from django.conf.urls import patterns, include, url
from django.contrib import admin

import enforta.settings as settings
import authentication_urls
import DocApproval.views.common as common_views

admin.autodiscover()

urlpatterns = patterns('',
                       #admin section
                       url(r'^admin/?', include(admin.site.urls)),
                       #url(r'^admin/doc/?', include('django.contrib.admindocs.urls')),
                       url(r'^/?$', common_views.index, name="common.home_page"),
                       url(r'^quicktest/$', common_views.quicktest, name="common.quick_test"),

                       url(r'^accounts/', include(authentication_urls))
                       #url(r'^accounts/login/$', 'django.contrib.auth.views.login', name="Authentication.Login"),
                       #url(r'^accounts/logout/$', 'django.contrib.auth.views.login', name="Authentication.Login"),

)

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()

import logging

logger = logging.getLogger(__name__)
logger.debug(urlpatterns)
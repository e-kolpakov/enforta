from django.conf.urls import patterns, include, url
from django.contrib import admin

import authentication_urls
from DocApproval.views import common

admin.autodiscover()

urlpatterns = patterns('',
                       #admin section
                       url(r'^admin/?', include(admin.site.urls)),
                       #url(r'^admin/doc/?', include('django.contrib.admindocs.urls')),
                       url(r'^/?$', common.index, name="common.home_page"),
                       url(r'^quicktest/$', common.RequestEditView.as_view(), name="common.quick_test"),
                       url(r'^thanks/$', common.quicktest, name="common.thanks"),

                       url(r'^accounts/', include(authentication_urls))
                       #url(r'^accounts/login/$', 'django.contrib.auth.views.login', name="Authentication.Login"),
                       #url(r'^accounts/logout/$', 'django.contrib.auth.views.login', name="Authentication.Login"),

)

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()

import logging

logger = logging.getLogger(__name__)
logger.debug(urlpatterns)
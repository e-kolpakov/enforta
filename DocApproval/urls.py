from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

import DocApproval.views
import DocApproval.views.common as common_views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
       #admin section
       url(r'^admin/?', include(admin.site.urls)),
       #url(r'^admin/doc/?', include('django.contrib.admindocs.urls')),
       url('^/?$', common_views.index),
       url('^quicktest/?$', common_views.quicktest)
)

urlpatterns += staticfiles_urlpatterns()
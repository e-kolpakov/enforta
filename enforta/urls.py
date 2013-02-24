from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    #admin section
    #url(r'^admin/?', include(admin.site.urls)),
    #url(r'^admin/doc/?', include('django.contrib.admindocs.urls')),
    url('^/?$', "DocApproval.views.index"),
    url('^quicktest/?$', "DocApproval.views.quicktest")
)

urlpatterns += staticfiles_urlpatterns()
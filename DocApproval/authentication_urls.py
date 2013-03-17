from django.conf.urls import patterns, url

_supported_views = ('login', 'logout')

urlpatterns = patterns('',
                       *[
                           url(
                               r'^%s/$' % view,
                               'django.contrib.auth.views.%s' % view,
                               {'template_name': 'authentication/%s.html' % view},
                               name="authentication.%s" % view
                           )
                           for view in _supported_views
                       ]
)

import logging

logger = logging.getLogger(__name__)
logger.debug(urlpatterns)

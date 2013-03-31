from django.conf.urls import patterns, url
from names import Authentication as auth_names

_supported_views = {'login': auth_names.LOGIN, 'logout': auth_names.LOGOUT}

urlpatterns = patterns(
    '',
    *[
        url(
            r'^%s/$' % view,
            'django.contrib.auth.views.%s' % view,
            {'template_name': 'authentication/%s.html' % view},
            name=url_name
        )
        for (view, url_name) in _supported_views.items()
    ]
)


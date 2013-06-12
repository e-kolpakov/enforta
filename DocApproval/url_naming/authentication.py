from django.conf.urls import patterns, url
from names import Authentication as auth_names

_supported_views = {
    'DocApproval.views.authentication.login': {'name': auth_names.LOGIN, 'url': 'login'},
    'django.contrib.auth.views.logout': {'name': auth_names.LOGOUT, 'url': 'logout'}
}

urlpatterns = patterns(
    '',
    *[
        url(
            r'^%s/$' % params['url'],
            view,
            {'template_name': 'authentication/{0}.html'.format(params['url'])},
            name=params['name']
        )
        for (view, params) in _supported_views.items()
    ]
)


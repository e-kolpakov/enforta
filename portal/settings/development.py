from base import LOGGING

ADMINS = ()

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'docapproval',
        'USER': 'docapprovaluser',
        'PASSWORD': '12345',
        'HOST': 'localhost',
        'PORT': '',
    }
}

for key in LOGGING['loggers'].keys():
    if key not in ('weasyprint', 'django.request', 'DocApproval.middleware'):
        LOGGING['loggers'][key]['level'] = 'DEBUG'

EMAIL_HOST = 'mailtrap.io'
EMAIL_HOST_USER = 'docapproval-9be468b6c99f0863'
EMAIL_HOST_PASSWORD = '1e2e916fef05dfad'
EMAIL_PORT = '25'
EMAIL_USE_TLS = False
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER



CELERYBEAT_SCHEDULE = {}

# class InvalidVarException(object):
#     def __mod__(self, missing):
#         try:
#             missing_str = unicode(missing)
#         except:
#             missing_str = 'Failed to create string representation'
#         raise Exception('Unknown template variable %r %s' % (missing, missing_str))
#
#     def __contains__(self, search):
#         if search == '%s':
#             return True
#         return False


# TEMPLATE_DEBUG = True
# TEMPLATE_STRING_IF_INVALID = InvalidVarException()
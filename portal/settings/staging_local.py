from base import LOGGING, format_broker, AMQP_USER, AMQP_PASS, AMQP_HOST, AMQP_PORT

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'docapproval_staging',
        'USER': 'docapprovaluser',
        'PASSWORD': '12345',
        'HOST': 'localhost',
        'PORT': '',
    }
}

EMAIL_HOST = 'mailtrap.io'
EMAIL_HOST_USER = 'docapproval-9be468b6c99f0863'
EMAIL_HOST_PASSWORD = '1e2e916fef05dfad'
EMAIL_PORT = '25'
EMAIL_USE_TLS = False
EMAIL_REDIRECT = 'redirect@localhost'
ROOT_URL = "http://docapproval.ru:8080"
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

AMQP_VHOST = 'docapprovalnotifications-staging_local'
BROKER_URL = format_broker(AMQP_USER, AMQP_PASS, AMQP_HOST, AMQP_PORT, AMQP_VHOST)

for key in LOGGING['loggers'].keys():
    if key not in ('weasyprint', 'django.request', 'DocApproval.middleware'):
        LOGGING['loggers'][key]['level'] = 'DEBUG'

MEDIA_ROOT = "/var/uploads/doc-approval-staging"
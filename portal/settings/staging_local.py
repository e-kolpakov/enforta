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
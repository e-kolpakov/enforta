import os
from base import LOGGING_DIRECTORY

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

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
    },
    'formatters': {
        'verbose': {
            'format': '%(asctime)s %(module)s [%(levelname)s] %(process)d %(thread)d %(message)s'
        },
        'generic': {
            'format': '%(asctime)s %(name)s->%(funcName)s:%(lineno)d [%(levelname)s]: %(message)s'
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOGGING_DIRECTORY, 'django.log'),
            'maxBytes': 102400,
            'backupCount': 1,
            'formatter': 'generic',
            'encoding': 'UTF-8'
        },
        'sql': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOGGING_DIRECTORY, 'sql.log'),
            'maxBytes': 102400,
            'backupCount': 0,
            'formatter': 'generic',
            'encoding': 'UTF-8'
        },
        'celery_tasks': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOGGING_DIRECTORY, 'celery.log'),
            'maxBytes': 1024000,
            'backupCount': 4,
            'formatter': 'generic',
            'encoding': 'UTF-8'
        }
    },
    'loggers': {
        '': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': False
        },
        'weasyprint': {
            'handlers': ['file'],
            'level': 'WARNING',
            'propagate': False
        },
        'django.db.backends': {
            'handlers': ['sql'],
            'level': 'DEBUG',
            'propagate': False
        },
        'DocApproval.middleware': {
            'handlers': ['file'],
            'level': 'WARNING',
            'propagate': False
        },
        'DocApproval': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': False
        },
        'DocApprovalNotifications': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': False
        },
        'DocApprovalNotifications.tasks': {
            'handlers': ['celery_tasks'],
            'level': 'DEBUG',
            'propagate': False
        },
        'django.request': {
            'handlers': ['mail_admins', 'file'],
            'level': 'ERROR',
            'propagate': True,
        }
    }
}
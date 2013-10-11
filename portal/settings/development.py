import os
from base import LOGGING_DIRECTORY

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

# LOGGING_DIRECTORY = "log"

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
    },
    'loggers': {
        '': {
            'handlers': ['file'],
            'level': 'DEBUG',
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
        'DocApproval.middleware.RequireLoginMiddleware': {
            'handlers': ['file'],
            'level': 'WARNING',
            'propagate': False
        },
        'DocApproval': {
            'handlers': ['file'],
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
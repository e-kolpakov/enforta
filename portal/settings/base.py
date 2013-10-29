# Django settings for portal project.
import os
import django
import djcelery

DEBUG = False
TEMPLATE_DEBUG = DEBUG

PROJECT_PATH = '/'.join(os.path.dirname(__file__).split('/')[0:-1])
DJANGO_ROOT = os.path.dirname(os.path.realpath(django.__file__))

# Administrator defined settings - feel free to customize as needed
# Mandatory settings
# FQDN or IP required here
ALLOWED_HOSTS = '*'

# Optional settings
ADMINS = (
# ('Your Name', 'your_email@example.com'),
)

LOGGING_DIRECTORY = os.path.join(PROJECT_PATH, "../log")

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Moscow'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'ru-ru'

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = "/var/uploads/doc-approval"
# End of administrator defined options

MANAGERS = ADMINS

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PROJECT_PATH, 'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
# Put strings here, like "/home/html/static" or "C:/www/django/static".
# Always use forward slashes, even on Windows.
# Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '!^8n+z3%*^2_d9b3ef58#!x-u9d$we5djt!7^vhkg-!e6uqtgi'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'reversion.middleware.RevisionMiddleware',

    'DocApproval.middleware.RequireLoginMiddleware',
    # 'DocApproval.middleware.MenuMiddleware',
    'DocApproval.middleware.SignatureCheckMiddleware'
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "DocApproval.menu.menu_context_processor"
)

FILE_UPLOAD_HANDLERS = (
    # "DocApproval.utilities.file_upload.BasicFileUploadHandler",
    "django.core.files.uploadhandler.MemoryFileUploadHandler",
    "django.core.files.uploadhandler.TemporaryFileUploadHandler"
)

# Authentication related
# using named urls
LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = 'common.home_page' # we want to land on index after login
LOGIN_REQUIRED_URLS = (".*",)
LOGIN_REQUIRED_URLS_EXCEPTIONS = (LOGIN_URL, "/admin", STATIC_URL, MEDIA_URL, '/requests/approval_sheet/42')

ROOT_URLCONF = 'portal.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'portal.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH, 'DocApproval/templates')
)

# installed apps are added at bottom
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

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
    },
    'loggers': {
        '': {
            'handlers': ['file'],
            'level': 'WARNING',
            'propagate': False
        },
        'weasyprint': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': False
        },
        'DocApproval': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': False
        },
        'DocApprovalNotifications': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': False
        },
        'django.request': {
            'handlers': ['mail_admins', 'file'],
            'level': 'ERROR',
            'propagate': True,
        }
    }
}

# Application specific settings

#reversion
INSTALLED_APPS += ('reversion',)

#south
INSTALLED_APPS += ('south',)

# guardian
INSTALLED_APPS += ('guardian',)
ANONYMOUS_USER_ID = -1

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend', # this is default
    'guardian.backends.ObjectPermissionBackend',
)

GUARDIAN_RENDER_403 = True

#djcelery
INSTALLED_APPS += ('djcelery',)
BROKER_URL = 'amqp://rabbit_notifier:rabbit_notifier_pass@localhost:5672/docapprovalnotifications'
CELERY_RESULT_BACKEND = 'amqp'
CELERY_TASK_RESULT_EXPIRES = 3600
djcelery.setup_loader()


#DocApproval
INSTALLED_APPS += ('DocApproval',)

# nothing funny. Governs usage of python-magic for checking filetypes.
# If set to true, python-magic is used, which is more secure, but might be more resource cosuming as well
USE_MAGIC = True

MAX_FILE_SIZE = 5120

ALLOWED_MIME_TYPES = (
    'application/pdf',
    'application/x-pdf',
    'image/tiff',
    'image/x-tiff',
    'image/jpeg',
    'image/pjpeg',
    'application/msword',
    'application/excel',
    'application/vnd.ms-excel',
    'application/x-excel',
    'application/x-msexcel',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
)

# these files are essentially zipped xml, so magic misreports them as application/zip -
# thus the only way is to skip them
SKIP_MAGIC_FILE_TYPES = (
    'application/x-excel',
    'application/x-msexcel',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
)

# DocApprovalNotifications
INSTALLED_APPS += ('DocApprovalNotifications',)

NOTIFICATIONS_TIMEOUT = '2 days'

NOTIFICATIONS_FREQUENCY = '1 day'
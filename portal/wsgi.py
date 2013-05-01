"""
WSGI config for portal project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

"""
import os
from django.core.handlers.wsgi import WSGIHandler

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
#sys.path.insert(0, PROJECT_PATH)

if True:
    import portal.monitor as monitor

    def monitor_file(arg, dirname, names):
        for filename in names:
            filename, extension = os.path.splitext(filename)
            monitor.track(os.path.join(dirname, filename))

    monitor.start(interval=1.0)
    os.path.walk(PROJECT_PATH, monitor_file, None)
    os.path.walk(os.path.join(PROJECT_PATH, '../DocApproval'), monitor_file, None)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "portal.settings")

# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
_application = WSGIHandler()

def application(environ, start_response):
    os.environ['EnvironmentType'] = environ['EnvironmentType']
    return _application(environ, start_response)

# Apply WSGI middleware here.
# from helloworld.wsgi import HelloWorldApplication
# application = HelloWorldApplication(application)

import re
import logging

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from DocApproval.messages import ProfileMessages
from DocApproval.models.common import Groups

from .menu import MenuManager


#taken from http://stackoverflow.com/questions/2164069/best-way-to-make-djangos-login-required-the-default
class RequireLoginMiddleware(object):
    """
    Middleware component that wraps the login_required decorator around
    matching URL patterns. To use, add the class to MIDDLEWARE_CLASSES and
    define LOGIN_REQUIRED_URLS and LOGIN_REQUIRED_URLS_EXCEPTIONS in your
    settings.py. For example:
    ------
    LOGIN_REQUIRED_URLS = (
        r'/topsecret/(.*)$',
    )
    LOGIN_REQUIRED_URLS_EXCEPTIONS = (
        r'/topsecret/login(.*)$',
        r'/topsecret/logout(.*)$',
    )
    ------
    LOGIN_REQUIRED_URLS is where you define URL patterns; each pattern must
    be a valid regex.

    LOGIN_REQUIRED_URLS_EXCEPTIONS is, conversely, where you explicitly
    define any exceptions (like login and logout URLs).
    """


    def __init__(self):
        self.required = tuple(re.compile(url) for url in settings.LOGIN_REQUIRED_URLS)
        self.exceptions = tuple(re.compile(url) for url in settings.LOGIN_REQUIRED_URLS_EXCEPTIONS)

    def process_view(self, request, view_func, view_args, view_kwargs):
        logger = logging.getLogger(__name__ + '.' + self.__class__.__name__)

        logger.debug("Processing view '{0}.{1}' with args {2} and kwargs {3}".format(
            view_func.__module__, view_func.__name__, view_args, view_kwargs
        ))
        # No need to process URLs if user already logged in
        if request.user.is_authenticated():
            logger.debug("Already authenticated as {0}".format(request.user.username))
            return None

        if hasattr(view_func, 'is_public') and view_func.is_public:
            logger.debug("View is public")
            return None

        # An exception match should immediately return None
        for url in self.exceptions:
            if url.match(request.path):
                logger.debug("URL matched exception %s" % url.pattern)
                return None

        # Requests matching a restricted URL pattern are returned
        # wrapped with the login_required decorator
        for url in self.required:
            if url.match(request.path):
                logger.debug("Login required")
                return login_required(view_func)(request, *view_args, **view_kwargs)

        # Explicitly return None for all non-matching requests
        return None


class MenuMiddleware(object):
    def process_view(self, request, view_func, view_args, view_kwargs):
        logger = logging.getLogger(__name__ + '.' + self.__class__.__name__)
        if view_func.__module__.split('.')[0] != 'DocApproval':
            return None
        logger.debug("Processing view '{0}.{1}' with args {2} and kwargs {3}".format(
            view_func.__module__, view_func.__name__, view_args, view_kwargs
        ))
        request.menu_manager = MenuManager(request.user)
        return None


class SignatureCheckMiddleware(object):
    def process_view(self, request, view_func, view_args, view_kwargs):
        logger = logging.getLogger(__name__ + '.' + self.__class__.__name__)
        if view_func.__module__.split('.')[0] != 'DocApproval':
            return None
        logger.debug("Processing view '{0}.{1}' with args {2} and kwargs {3}".format(
            view_func.__module__, view_func.__name__, view_args, view_kwargs
        ))
        if request.user.groups.filter(name=Groups.APPROVERS).exists():
            if not request.user.profile.sign and not request.COOKIES.get('ignore_empty_signature'):
                messages.add_message(request, messages.WARNING, ProfileMessages.SIGNATURE_EMPTY)
        return None
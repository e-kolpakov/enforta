__author__ = 'john'
from django.conf import settings

from base_test import BaseTest
from ..url_naming.names import *


class AuthMiddleWareTest(BaseTest):
    def test_not_logged_in(self):
        self._request_and_check(Common.HOME, 302)

    def test_not_logged_in_exceptions(self):
        self._request_and_check(settings.LOGIN_REQUIRED_URLS_EXCEPTIONS[0], 200, is_url=True)

    def test_not_logged_in_public(self):
        #TODO: rewrite to use real public view
        self._request_and_check('/quicktest/', 200, is_url=True)

    def test_logged_in_private(self):
        self.login()
        resp = self._request_and_check(Common.HOME, 200)
        self.assertEqual(resp.context['user'].username, 'user1')

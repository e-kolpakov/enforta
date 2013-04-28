__author__ = 'john'

from base_test import BaseTest
from ..url_naming.names import *


class URLSmokeTest(BaseTest):
    def setUp(self):
        super(URLSmokeTest, self).setUp()
        self.login()

    def test_index(self):
        self._request_and_check(Common.HOME, 200)

    def test_request(self):
        self._request_and_check(Request.ARCHIVE, 200)
        self._request_and_check(Request.ARCHIVE_YEAR, 200, year=2013)
        self._request_and_check(Request.ARCHIVE_MONTH, 200, month='01', year=2013)
        self._request_and_check(Request.CREATE, 200)
        self._request_and_check(Request.DETAILS, 200, pk=1)
        self._request_and_check(Request.UPDATE, 200, pk=1)
        self._request_and_check(Request.LIST, 200)
        self._request_and_check(Request.MY_APPROVALS, 200)
        self._request_and_check(Request.MY_REQUESTS, 200)

    def test_profile(self):
        self._request_and_check(Profile.MY_PROFILE, 200)
        self._request_and_check(Profile.PROFILE, 200, pk=1)

    def test_auth(self):
        self._request_and_check(Authentication.LOGIN, 200)
        self._request_and_check(Authentication.LOGOUT, 200)

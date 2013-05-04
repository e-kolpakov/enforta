from django.contrib.auth.models import User as AuthUser
from django.test import (TestCase)
from django.core.urlresolvers import (reverse)

from .. import models


class BaseTest(TestCase):
    USER1 = 'user1'
    USER2 = 'user2'
    APPROVER1 = 'approver1'
    APPROVER2 = 'approver2'
    ADMIN = 'admin'

    fixtures = ('start_data.yaml', 'test_data.yaml')

    default_user = USER1
    credentials = {
        'user1': ('user1', '1234'),
        'user2': ('user2', '1234'),
        'approver1': ('approver1', '1234'),
        'approver2': ('approver2', '1234'),
        'admin': ('admin', '&FJ2>Vvzyhm,#xM')
    }

    def login(self, user=None):
        effective_user = user if user else self.default_user
        username, password = self.credentials[effective_user]
        self.user = self.client.login(username=username, password=password)
        return self.user

    def logout(self):
        self.client.logout()

    def _get_user_profile(self, username):
        return AuthUser.objects.get(username__exact=username).profile

    def _request_and_check(self, url_name, expected_status_code, is_url=False, **view_kwargs):
        url = reverse(url_name, kwargs=view_kwargs) if not is_url else url_name
        resp = self.client.get(url, **view_kwargs)
        self.assertEqual(resp.status_code, expected_status_code)
        return resp


class LoggedInTest(BaseTest):
    default_user = BaseTest.USER1

    def setUp(self):
        self.login()
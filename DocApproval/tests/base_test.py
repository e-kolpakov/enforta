from django.test import (TestCase)
from django.core.urlresolvers import (reverse)

from .. import models


class BaseTest(TestCase):
    fixtures = ('start_data.yaml', 'test_data.yaml')

    default_user = 'user1'
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

    def _get_user_profile(self, user_id):
        return models.UserProfile.objects.get(pk=user_id)

    def _request_and_check(self, url_name, expected_status_code, is_url=False, **view_kwargs):
        url = reverse(url_name, kwargs=view_kwargs) if not is_url else url_name
        resp = self.client.get(url, **view_kwargs)
        self.assertEqual(resp.status_code, expected_status_code)
        return resp


class LoggedInTest(BaseTest):
    def setUp(self):
        self.login()
from django.test import (TestCase)
from django.core.urlresolvers import (reverse)

from .. import models


class BaseTest(TestCase):
    fixtures = ('start_data.yaml', 'test_data.yaml')

    def login(self):
        self.user = self.client.login(username='user1', password='1234')

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
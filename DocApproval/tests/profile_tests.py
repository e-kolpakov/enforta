__author__ = 'john'
from django.core.urlresolvers import (reverse)

from base_test import BaseTest
from ..url_naming.names import *


class ProfileDetailsTest(BaseTest):
    def setUp(self):
        super(ProfileDetailsTest, self).setUp()

    def test_refuse_not_logged_in(self):
        trgt_user = self._get_user_profile(self.USER1)
        resp = self.client.get(reverse(Profile.PROFILE, kwargs={'pk': trgt_user.pk}), pk=trgt_user.pk)
        self.assertEqual(resp.status_code, 302)

    def test_non_existing_profile(self):
        self.login()
        resp = self.client.get(reverse(Profile.PROFILE, kwargs={'pk': 10000}), pk=10000)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['user_profile'], None)

    def test_allow_logged_in(self):
        self.login()
        trgt_user = self._get_user_profile(self.USER1)
        resp = self.client.get(reverse(Profile.MY_PROFILE))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['user_profile'], trgt_user)
from django.core.urlresolvers import reverse

from base_test import BaseTest
from ..url_naming.names import Common

class TestAuthentication(BaseTest):
    users = ('user1', 'user2', 'approver1', 'approver2', 'admin')

    def test_users_login(self):
        for user in self.users:
            self.assertTrue(self.login(user), msg="Login failed for user {}".format(user))
            self.logout()
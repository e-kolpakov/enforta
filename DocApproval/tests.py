"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import (TestCase )
from django.core.urlresolvers import (reverse, NoReverseMatch)
from django.conf import settings

from url_naming.names import *
import models


class BaseTest(TestCase):
    fixtures = ['test_data']

    def login(self):
        self.user = self.client.login(username='user1', password='1234')

    def _request_and_check(self, url_name, expected_status_code, is_url=False, **view_kwargs):
        url = reverse(url_name, kwargs=view_kwargs) if not is_url else url_name
        resp = self.client.get(url, **view_kwargs)
        self.assertEqual(resp.status_code, expected_status_code)
        return resp


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
        self._request_and_check(Profile.PROFILE, 200)

    def test_auth(self):
        self._request_and_check(Authentication.LOGIN, 200)
        self._request_and_check(Authentication.LOGOUT, 200)


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


class RequestCreateTest(BaseTest):
    def setUp(self):
        super(RequestCreateTest, self).setUp()
        self.login()

    def _check_form_errors(self, resp, form_key, errors_count):
        for key, value in errors_count.items():
            self.assertEqual(len(resp.context[form_key][key].errors), value)

    def test_get(self):
        resp = self._request_and_check(Request.CREATE, 200)
        self.assertTrue('form' in resp.context)

    def test_post(self):
        any_user_profile = models.UserProfile.objects.get(pk=6)
        # Junk Post
        resp = self.client.post(reverse(Request.CREATE), {'qwe': 'rty'})
        self.assertEqual(resp.status_code, 200)
        self._check_form_errors(resp, 'form', {'name': 1, 'city': 1, 'send_on_approval': 1})

        # Some fields missing
        resp = self.client.post(reverse(Request.CREATE), {'name': '123'})
        self.assertEqual(resp.status_code, 200)
        self._check_form_errors(resp, 'form', {'city': 1, 'send_on_approval': 1})

        #Invalid city
        resp = self.client.post(reverse(Request.CREATE),
                                {'name': '123', 'city': 10000, 'send_on_approval': any_user_profile.pk})
        self.assertEqual(resp.status_code, 200)
        self._check_form_errors(resp, 'form', {'name': 0, 'city': 1, 'send_on_approval': 0})

        #Valid post
        resp = self.client.post(reverse(Request.CREATE),
                                {'name': '123', 'city': 1, 'send_on_approval': any_user_profile.pk, 'comments': 'test'})
        self.assertEqual(resp.status_code, 200)
        self._check_form_errors(resp, 'form', {'name': 0, 'city': 0, 'send_on_approval': 0, 'comments': 0})


class TestRequestDetails(BaseTest):
    def setUp(self):
        super(TestRequestDetails, self).setUp()
        self.login()

    def test_missing_id(self):
        self.assertRaises(NoReverseMatch, lambda: self.client.get(reverse(Request.DETAILS)))

    def test_non_existing_id(self):
        resp = self.client.get(reverse(Request.DETAILS, kwargs={'pk': 10000}), pk=10000)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['request'], None)

    def test_existing_id(self):
        req = models.Request.objects.get(pk=1)
        resp = self.client.get(reverse(Request.DETAILS, kwargs={'pk': 1}), pk=1)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['request'], req)
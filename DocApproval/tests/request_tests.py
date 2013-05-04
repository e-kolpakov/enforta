"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
import StringIO

from django.core.urlresolvers import (reverse, NoReverseMatch)

from base_test import (BaseTest, LoggedInTest)
from ..url_naming.names import *
from .. import models
from ..views.request import ListRequestView


class RequestCreateTest(LoggedInTest):
    default_user = BaseTest.ADMIN

    def _check_form_errors(self, resp, form_key, errors_count):
        for key, value in errors_count.items():
            self.assertEqual(len(resp.context[form_key][key].errors), value,
                             "Errors mismatch for field {0}".format(key))

    def test_get(self):
        resp = self._request_and_check(Request.CREATE, 200)
        self.assertTrue('form' in resp.context)

    def test_post_junk(self):
        resp = self.client.post(reverse(Request.CREATE), {'qwe': 'rty'})
        self.assertEqual(resp.status_code, 200)
        self._check_form_errors(resp, 'form', {'name': 1, 'city': 1, 'send_on_approval': 1})

    def test_post_incomplete(self):
        resp = self.client.post(reverse(Request.CREATE), {'name': '123'})
        self.assertEqual(resp.status_code, 200)
        self._check_form_errors(resp, 'form', {'city': 1, 'send_on_approval': 1})

    def test_post_invalid_city(self):
        approver1 = self._get_user_profile(self.APPROVER1)
        resp = self.client.post(reverse(Request.CREATE),
                                {'request-name': '123', 'request-city': 10000,
                                 'request-send_on_approval': approver1.pk})
        self.assertEqual(resp.status_code, 200)
        self._check_form_errors(resp, 'form', {'name': 0, 'city': 1, 'send_on_approval': 0})

    def test_post_valid(self):
        approver1 = self._get_user_profile(self.APPROVER1)
        upl_file = StringIO.StringIO("test data")
        upl_file.name = 'documents/new/123.txt'
        resp = self.client.post(reverse(Request.CREATE), {
            'request-name': '123',
            'request-city': 1,
            'request-send_on_approval': approver1.pk,
            'request-comments': 'test',
            'contract-date': '2013-01-01',
            'contract-active_period': '1',
            'contract-document': upl_file
        })
        self.assertEqual(resp.status_code, 302)


class RequestDetailsTest(BaseTest):
    def test_missing_id(self):
        self.login()
        self.assertRaises(NoReverseMatch, lambda: self.client.get(reverse(Request.DETAILS)))

    def test_non_existing_id(self):
        self.login()
        resp = self.client.get(reverse(Request.DETAILS, kwargs={'pk': 10000}), pk=10000)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['doc_request'], None)

    def test_existing_id_allowed_creator(self):
        self.login('user2')
        req = models.Request.objects.get(pk=1)
        resp = self.client.get(reverse(Request.DETAILS, kwargs={'pk': 1}), pk=1)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['doc_request'], req)

    def test_existing_id_allowed_by_permission(self):
        self.login('admin')
        req = models.Request.objects.get(pk=1)
        resp = self.client.get(reverse(Request.DETAILS, kwargs={'pk': 1}), pk=1)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['doc_request'], req)

    def test_existing_id_not_allowed(self):
        self.login('user1')
        resp = self.client.get(reverse(Request.DETAILS, kwargs={'pk': 1}), pk=1)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['doc_request'], None)


class RequestListTest(LoggedInTest):
    def test_datatables_config(self):
        resp = self.client.get(reverse(Request.LIST))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['datatables_data'], Request.LIST_JSON)
        self.assertEqual(resp.context['datatables_config'], Request.LIST_JSON_CONF)

    def test_general_list(self):
        resp = self.client.get(reverse(Request.LIST))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['show_only'], None)

    def test_my_approvals(self):
        url_params = {ListRequestView.SHOW_ONLY_PARAM: ListRequestView.MY_APPROVALS}
        resp = self.client.get(reverse(Request.MY_APPROVALS, kwargs=url_params), **url_params)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['show_only'], ListRequestView.MY_APPROVALS)

    def test_my_requests(self):
        url_params = {ListRequestView.SHOW_ONLY_PARAM: ListRequestView.MY_REQUESTS}
        resp = self.client.get(reverse(Request.MY_REQUESTS, kwargs=url_params), **url_params)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['show_only'], ListRequestView.MY_REQUESTS)


# class RequestJsonTest(BaseTest):
#     json_url = reverse(Request.LIST_JSON)
#
#     def serialize_requests(self, request_list):
#         pass
#
#     def test_superuser_have_unlimited_access(self):
#         self.login('admin')

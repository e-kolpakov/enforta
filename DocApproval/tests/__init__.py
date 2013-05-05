__author__ = 'john'

from unittest import (TestSuite, TestLoader)

from url_tests import URLSmokeTest
from middleware_tests import AuthMiddleWareTest
from request_tests import (RequestCreateTest, RequestDetailsTest, RequestListTest)
from profile_tests import (ProfileDetailsTest)
from auth_tests import TestAuthentication


def suite():
    unit_test_cases = ()
    integration_test_cases = (
        URLSmokeTest,
        AuthMiddleWareTest,
        RequestCreateTest, RequestDetailsTest, ProfileDetailsTest, RequestListTest,
        TestAuthentication
    )
    all_test_cases = unit_test_cases + integration_test_cases
    test_loader = TestLoader()
    tests = [test_loader.loadTestsFromTestCase(case) for case in all_test_cases]
    return TestSuite(tests)
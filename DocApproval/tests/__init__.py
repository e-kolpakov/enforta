from unittest import (TestSuite, TestLoader)

from url_tests import URLSmokeTest
from middleware_tests import AuthMiddleWareTest
from request_tests import (RequestCreateTest, RequestDetailsTest, RequestListTest)
from profile_tests import (ProfileDetailsTest)
from auth_tests import TestAuthentication


def suite():
    test_cases = (
        URLSmokeTest,
        AuthMiddleWareTest,
        RequestCreateTest, RequestDetailsTest, ProfileDetailsTest, RequestListTest,
        TestAuthentication
    )
    test_loader = TestLoader()
    tests = [test_loader.loadTestsFromTestCase(case) for case in test_cases]
    return TestSuite(tests)
from datetime import datetime
from time import time, mktime
from unittest2 import TestCase
from django.contrib.auth.models import User
import json
try:
    from django.core import signing
except ImportError:
    from django_signed import signed
    signing = signed

from ..backends import SharedAuthBackend
from .. import settings

JSON_STR = """{"u": "testSharedAuthUser", "e": "test.user@nowhere.com", "l": "User", "f": "Test"}"""
SIGNED_STR = 'eyJlIjoidGVzdC51c2VyQG5vd2hlcmUuY29tIiwidSI6InRlc3RTaGFyZWRBdXRoVXNlciIsImwiOiJVc2VyIiwiZiI6IlRlc3QifQ.1Fzn4pRbQ9sWQRRzQ504XuUPU0Q'
settings.SECRET = '1234'

class TestStaticMethods(TestCase):
    """
    Test static functions
    """

    def setUp(self):
        """
        Set up the authtoken testcase
        """
        self.user = User(username='testSharedAuthUser', email='test.user@nowhere.com', last_name='User',
                         first_name='Test')
        self.user.save()

    def tearDown(self):
        """
        Tear down the authtoken testcase
        """
        self.user.delete()

    def testUserFromJsonStr(self):
        """
        Ensure we can properly decode a json string
        """
        u = SharedAuthBackend.userFromJsonStr(JSON_STR)
        self.assertEqual(self.user, u)


class ClearSharedAuthBackendTest(TestCase):
    """
    Test SharedAuthBackend class functionality
    """

    def setUp(self):
        """
        Set up the authtoken testcase
        """
        self.user = User(username='testSharedAuthUser', email='test.user@nowhere.com', last_name='User',
                         first_name='Test')
        self.user.save()

    def tearDown(self):
        """
        Tear down the authtoken testcase
        """
        self.user.delete()


    def testJsonSharedAuthBackendFromUser(self):
        """
        ensure we can build a cookie sdtring for a user
        """
        self.assertEqual(json.loads(SharedAuthBackend.getCookieStr(self.user)), json.loads(JSON_STR))

        def testSignedSharedAuthBackendFromUser(self):
            """
            ensure we can build a cookie string for a user
            """
            self.assertEqual(signing.loads(SharedAuthBackend.getCookieStr(self.user)), signing.loads(self.signed_str))

        def testFindUserByUserName(self):
            """
            ensure that we can find a user that already exists if we have a cookie string
            """
            self.assertEqual(SharedAuthBackend.authenticate(cookie_str=JSON_STR), self.user)

        def testFindUserByEmail(self):
            """
            ensure that we can create a user that does not yet exist if we have a cookie string
            """
            cookieStr = """{"u": "testSharedAuthUser3", "e": "test.user@nowhere.com", "l": "User", "f": "Test"}"""
            t = SharedAuthBackend(cookieStr)
            self.assertEqual(t.user, self.user)

        def testCreateUserFromString(self):
            """
            ensure that we can create a user that does not yet exist if we have a cookie string
            """
            cookieStr = """{"u": "testSharedAuthUser2", "e": "test.user2@nowhere.com", "l": "User", "f": "Test"}"""
            t = SharedAuthBackend(cookieStr)
            self.assertEqual(t.user.username, 'testSharedAuthUser2')
            self.assertEqual(t.user.email, 'test.user2@nowhere.com')
            self.assertEqual(t.user.last_name, 'User')
            self.assertEqual(t.user.first_name, 'Test')
            self.assertNotEqual(t.user, self.user)
            t.user.delete()

        def testInvalidSharedAuthBackend(self):
            """
            test parsing back the results from a bad cookie into an authtoken

            should have the same results as an Empty init
            """
            cookie = 'badCookieString'
            with self.assertRaises(ValueError):
                SharedAuthBackend.authenticate(cookie_str=cookie)

class SignedSharedAuthBackendTest(TestCase):
    """
    Test SharedAuthBackend class functionality
    """

    def setUp(self):
        """
        Set up the authtoken testcase
        """
        self.user = User(username='testSharedAuthUser', email='test.user@nowhere.com', last_name='User',
                         first_name='Test')
        self.user.save()

    def tearDown(self):
        """
        Tear down the authtoken testcase
        """
        self.user.delete()

    def testSharedAuthBackendFromUser(self):
        """
        ensure we can build a cookie string for a user
        """
        self.assertEqual(signing.loads(SharedAuthBackend.getCookieStr(self.user)),
                         signing.loads(SIGNED_STR))

    def testFindUserByUserName(self):
        """
        ensure that we can find a user that already exists if we have a cookie string
        """
        self.assertEqual(SharedAuthBackend.authenticate(cookie_str=SIGNED_STR), self.user)

    def testInvalidCookieStr(self):
        """
        test parsing back the results from a bad cookie into an authtoken

        should have the same results as an Empty init
        """

        cookie = 'badCookieString'
        with self.assertRaises(ValueError):
            SharedAuthBackend.authenticate(cookie_str=cookie)


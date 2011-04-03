from django.test import TestCase
from django.http import HttpRequest, HttpResponse

from .. import logger, settings
from ..middleware import SharedAuthProviderMiddleware
from ..middleware import SharedAuthConsumerMiddleware

class TestSharedAuthProviderMiddleware(TestCase):
    """
    test basic functionality for the SharedAuthProviderMiddleware
    """
    def setUp(self):
        self.middleware = SharedAuthProviderMiddleware()

    def testProvider(self):
        """
        test the provider
        """
        req = HttpRequest()
        resp = HttpResponse()
        req.session = None
        self.middleware.process_response(req, resp)
        #self.assertNotEqual(None, getattr(req, settings.COOKIE_NAME, None))

class TestSharedAuthConsumerMiddleware(TestCase):
    """
    test basic shared auth consumer functionality
    """
    def setUp(self):
        self.middleware = SharedAuthConsumerMiddleware()

    def testConsumer(self):
        """
        do some stuff
        """
        req = HttpRequest()
        resp = HttpResponse()
        self.middleware.process_request(req)


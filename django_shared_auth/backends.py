from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from . import settings
from django.core.urlresolvers import get_callable
try:
    from django_signed import signed
except:
    logger.warning('django_signed unavailable, SIGNED mode unavailable')
from django.utils import simplejson as json


class SharedAuthBackend(ModelBackend):
    """
    Fill in the authenticate method
    """

    @staticmethod
    def authenticate(cookie_str=None):
        """
        authenticate via a cookie string
        """
        if cookie_str == None:
            return None

        if settings.SIGNED:
            return SharedAuthBackend.userFromSignedStr(cookie_str)
        else:
            return SharedAuthBackend.userFromJsonStr(cookie_str)

    @staticmethod
    def getCookieStr(user):
        """
        create the cookie string for a user
        """
        if settings.SIGNED:
            return SharedAuthBackend.signedStrFromUser(user)
        else:
            return SharedAuthBackend.jsonStrFromUser(user)

    @staticmethod
    def dictFromUser(user):
        """
        create a shared auth cookie from a user
        """
        c = dict()
        c['u'] = user.username
        c['f'] = user.first_name
        c['l'] = user.last_name
        c['e'] = user.email
        return c

    @staticmethod
    def userFromDict(userdict):
        """
        load or create a user record from a shared auth cookie
        """

        user_class = getattr(settings, 'USER_CLASS', 'django.contrib.auth.models.User')
        user_class = get_callable(user_class)
            
        results = user_class.objects.filter(username=userdict['u'])
        if results.count() == 1:
            return results[0]

        results = user_class.objects.filter(email=userdict['e'])
        if results.count() == 1:
            return results[0]

        u = user_class(username=userdict['u'],
                 first_name=userdict['f'],
                 last_name=userdict['l'],
                 email=userdict['e'])
        u.save()
        return u

    @staticmethod
    def userFromSignedStr(signed_str):
        """
        encode a sign a string
        """
        return SharedAuthBackend.userFromDict(signed.loads(signed_str))

    @staticmethod
    def signedStrFromUser(user):
        """
        decode and verify signature of string
        """
        return signed.dumps(SharedAuthBackend.dictFromUser(user))

    @staticmethod
    def userFromJsonStr(json_str):
        """
        decode a json string to a user
        """
        return SharedAuthBackend.userFromDict(json.loads(json_str))

    @staticmethod
    def jsonStrFromUser(user):
        """
        encode a sign a string
        """
        return json.dumps(SharedAuthBackend.dictFromUser(user))

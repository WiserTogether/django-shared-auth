from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from . import settings, logger
from django.core.urlresolvers import get_callable
try:
    from django_signed import signed
except:
    logger.warning('django_signed unavailable, SIGNED mode unavailable')
import json


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
        logger.debug('extracting user record from signed cookie')
        dct = signed.loads(signed_str)

        should_continue = True
        extra_params_consumer = getattr(settings, 'EXTRA_PARAMS_CONSUMER', None)
        if extra_params_consumer:
            logger.debug('attempting to execute EXTRA_PARAMS_CONSUMER %s'%(extra_params_consumer))
            extra_params_consumer = get_callable(extra_params_consumer)
            should_continue, user = extra_params_consumer(dct['u'], dct['extra_params'])
            logger.debug('call to EXTRA_PARAMS_CONSUMER complete, should_continue = %s' %(str(should_continue),))

        if should_continue:
            user = SharedAuthBackend.userFromDict(dct)
            logger.debug('got user %s' (user.username))
            # Call extra params consumer again so that it can handle params after the user is created
            if extra_params_consumer:
                should_continue, user = extra_params_consumer(dct['u'], dct['extra_params'])
            return user
        else:
            return None

    @staticmethod
    def signedStrFromUser(user):
        """
        decode and verify signature of string
        """
        dct = SharedAuthBackend.dictFromUser(user)

        extra_params_provider = getattr(settings, 'EXTRA_PARAMS_PROVIDER', None)
        if extra_params_provider:
            extra_params_provider = get_callable(extra_params_provider)
            dct['extra_params'] = extra_params_provider(user)

        return signed.dumps(dct)

    @staticmethod
    def userFromJsonStr(json_str):
        """
        decode a json string to a user
        """
        dct = json.loads(json_str)

        should_continue = True
        extra_params_consumer = getattr(settings, 'EXTRA_PARAMS_CONSUMER', None)
        if extra_params_consumer:
            extra_params_consumer = get_callable(extra_params_consumer)
            should_continue, user = extra_params_consumer(dct['extra_params'])

        if should_continue:
            user = SharedAuthBackend.userFromDict(dct)
            # Call extra params consumer again so that it can handle params after the user is created
            if extra_params_consumer:
                should_continue, user = extra_params_consumer(dct['u'], dct['extra_params'])
            return user
        else:
            return None

    @staticmethod
    def jsonStrFromUser(user):
        """
        encode a sign a string
        """
        dct = SharedAuthBackend.dictFromUser(user)

        extra_params_provider = getattr(settings, 'EXTRA_PARAMS_PROVIDER', None)
        if extra_params_provider:
            extra_params_provider = get_callable(extra_params_provider)
            dct['extra_params'] = extra_params_provider(user)

        return json.dumps(dct)

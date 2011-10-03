import time
from django.contrib import auth

from django.utils.http import cookie_date
from django.http import HttpResponseRedirect, HttpResponseServerError

from . import settings, logger
from .backends import SharedAuthBackend

LOGGIN = False

if LOGGIN:
    import logging
    #logging.basicConfig()
    logger = logging.getLogger(__name__)

class SharedAuthConsumerMiddleware(object):
    """
    Consume shared auth cookies and logging the user in automatically, and
    creating the user account if necessary

    To use, add to MIDDLEWARE_CLASSES after the django AuthenticationMiddleware
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django_shared_auth.middleware.SharedAuthConsumerMiddleware',

    and add the Backend to AUTHENTICATION_BACKENDS
        AUTHENTICATION_BACKENDS = (
            'django.contrib.auth.backends.ModelBackend',
            'django_shared_auth.backends.SharedAuthBackend',
        )
    """
    def process_request(self, request):
        try:
            if request.COOKIES.has_key(settings.COOKIE_NAME):
                cookie_str = request.COOKIES.get(settings.COOKIE_NAME)
                setattr(request, settings.COOKIE_NAME, cookie_str)
                # If the user is already authenticated and that user is the user we are
                # getting passed in the headers, then the correct user is already
                # persisted in the session and we don't need to continue.

<<<<<<< HEAD
                logger.debug('shared auth token found, authenticating user')
=======
                if LOGGIN:
                    logger.debug('shared auth token found, authenticating user')
>>>>>>> viraj-github/master
                # store the cookie on the request so the provider doesn't try to set
                # a new one on every request
                # We are seeing this user for the first time in this session, attempt
                # to authenticate the user.
                user = auth.authenticate(cookie_str=cookie_str)

<<<<<<< HEAD
                #if request.user.is_authenticated() and request.user == user:
                #    logger.debug('user is already properly authenticated')
                #    return

                if user:
                    logger.debug('user exists, forwarding to backend')
=======
                if request.user.is_authenticated() and request.user == user:
                    if LOGGIN:
                        logger.debug('user is already properly authenticated')
                    return

                if user:
                    if LOGGIN:
                        logger.debug('user exists, forwarding to backend %s' % user)
>>>>>>> viraj-github/master
                    # User is valid.  Set request.user and persist user in the session
                    # by logging the user in.
                    request.user = user
                    auth.login(request, user)
<<<<<<< HEAD
                    logger.debug('user logged in, session is %s' %(request.session))
                    request.session['SHARED_AUTH_USER'] = True
                else:
                    logger.debug('invalid user, redirecting to failure notice')
=======
                    if LOGGIN:
                        logger.debug('user logged in, session is %s' %(request.session))
                    request.session['SHARED_AUTH_USER'] = True
                else:
                    if LOGGIN:
                        logger.debug('invalid user, redirecting to failure notice')
>>>>>>> viraj-github/master
                    redirect_to = getattr(settings, 'AUTHENTICATION_FAIL_REDIRECT_URL', None)
                    if redirect_to:
                        return HttpResponseRedirect(redirect_to)
            else:
                if request.user.is_authenticated() \
                        and hasattr(request, 'session') \
                        and request.session.has_key('SHARED_AUTH_USER'):
<<<<<<< HEAD
                    logger.debug('user is authenticated via shared_auth without a token, logging out')
                    auth.logout(request)
        except Exception, e:
            logger.exception(e)
            return response
=======
                    if LOGGIN:
                        logger.debug('user is authenticated via shared_auth without a token, logging out')
                    auth.logout(request)
        except Exception, e:
            if LOGGIN:
                logger.exception(e)
            return HttpResponseServerError('ERROR: Shared auth configuration error')
>>>>>>> viraj-github/master

class SharedAuthProviderMiddleware(object):
    """
    Create shared auth cookies for logged-in users, allowing other sites
    sharing the COOKIE_DOMAIN to automatically log in users with the
    SharedAuthConsumerMiddleware and SharedAuthBackend

    add to MIDDLEWARE_CLASSES before the django AuthenticationMiddleware
        MIDDLEWARE_CLASSES = (
            ...
            'django_shared_auth.middleware.SharedAuthProviderMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            ...
        )
    """
    def process_response(self, request, response):
        """
        process the response, adding appropriate set-cookie
        headers if necessary.

        If there is an authenticated user, a cookie should be added
        representing that user's login information to pluck.

        If the authenticated user disappears but the at cookie remains,
        the at cookie should be deleted.
        """
        try:
            modify = False
            if 'UPDATE_SHAREDAUTH_COOKIE' in dict(response.items()):
<<<<<<< HEAD
                logger.debug('UPDATE_SHAREDAUTH_COOKIE found, forcing cookie update')
=======
                if LOGGIN:
                    logger.debug('UPDATE_SHAREDAUTH_COOKIE found, forcing cookie update')
>>>>>>> viraj-github/master
                response.__delitem__('UPDATE_SHAREDAUTH_COOKIE')
                modify = True

            if getattr(request, 'session', None) and \
                    hasattr(request, 'user') and \
                    request.user.is_authenticated() and \
                    (modify or not request.COOKIES.has_key(settings.COOKIE_NAME)):

                if request.session.get_expire_at_browser_close():
                    max_age = None
                    expires = None
                else:
                    max_age = request.session.get_expiry_age()
                    expires_time = time.time() + max_age
                    expires = cookie_date(expires_time)
                response.set_cookie(settings.COOKIE_NAME,
                        SharedAuthBackend.getCookieStr(request.user),
                        max_age=max_age,
                        expires=expires,
                        domain=settings.COOKIE_DOMAIN,
                        path=settings.COOKIE_PATH,
                        secure=settings.SECURE)
            if getattr(request, 'session', None) and \
                    not (hasattr(request, 'user') and \
                    request.user.is_authenticated()) and \
                    request.COOKIES.has_key(settings.COOKIE_NAME):
                response.delete_cookie(settings.COOKIE_NAME, path=settings.COOKIE_PATH, domain=settings.COOKIE_DOMAIN)
            return response
        except Exception, e:
<<<<<<< HEAD
            logger.exception(e)
=======
            if LOGGIN:
                logger.exception(e)
>>>>>>> viraj-github/master
            return response


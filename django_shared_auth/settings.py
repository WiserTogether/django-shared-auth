from django.conf import settings
__doc__ = """
settings
"""

COOKIE_PATH=getattr(settings, 'SHARED_AUTH_COOKIE_PATH', '/')
COOKIE_DOMAIN=getattr(settings, 'SHARED_AUTH_COOKIE_PATH', None)
COOKIE_NAME=getattr(settings, 'SHARED_AUTH_COOKIE_NAME', 'dsatok')
SIGNED=getattr(settings, 'SHARED_AUTH_SIGNED', True)
SECURE=getattr(settings, 'SESSION_COOKIE_SECURE', True)

if SIGNED:
    try:
        import django_signed
    except:
        logger.warn('django_signed not in PYTHONPATH, signing unavailable')
        SIGNED=False

# If your application uses a custom user class other than 
# django.contrib.auth.models.User, specify the class name
# The custom class will be provided only with the following attributes
# 1. username
# 2. email
# 3. first_name
# 4. last_name
USER_CLASS=getattr(settings, 'SHAREDAUTH_USER_CLASS', 'django.contrib.auth.models.User')

# The EXTRA_PARAMS_PROVIDER should return a query-string representation of extra information
EXTRA_PARAMS_PROVIDER=getattr(settings, 'SHAREDAUTH_EXTRA_PARAMS_PROVIDER', None)

# The EXTRA_PARAMS_CONSUMER should return a query-string representation of extra information
EXTRA_PARAMS_CONSUMER=getattr(settings, 'SHAREDAUTH_EXTRA_PARAMS_CONSUMER', None)

# If the user authentication fails, redirect the user to this URL
AUTHENTICATION_FAIL_REDIRECT_URL=getattr(settings, 'SHAREDAUTH_AUTHENTICATION_FAIL_REDIRECT_URL', None)
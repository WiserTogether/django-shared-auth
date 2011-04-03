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


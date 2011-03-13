Shared authentication via secure domain cookies.

This module implements a simple single-sign-on mechanism based on
secure cookies. On sites providing authentication, logged in users
have a cookie set. This cookie is optionally encrypted with a shared
secret. Sites consuming authentication can use the provided middleware
to ensure that users are created and logged in automatically based on
the presence of the cookie.

Signed cookies are enabled by default, but require django_signed from
https://github.com/simonw/django-signed

If you're going to run multiple django instances on the same domain, you'll
probably want to set your SESSION_COOKE_NAME, SESSION_COOKIE_DOMAIN or
SESSION_COOKIE_PATH so they aren't all trying to use the same session.

To provide authentication:
    add  the SharedAuthProviderMiddleware to MIDDLEWARE_CLASSES before the
    django AuthenticationMiddleware. You do not need to include the backend
    unless you're planning to also consume logins.

    MIDDLEWARE_CLASSES = (
        ...
        'django_sharedauth.middleware.SharedAuthProviderMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        ...
    )

To consume authentication:
    Add SharedAuthConsumerMiddleware to MIDDLEWARE_CLASSES after the
    django AuthenticationMiddleware.

    MIDDLEWARE_CLASSES = (
        ...
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django_sharedauth.middleware.SharedAuthConsumerMiddleware',
        ...
    )

    Add the SharedAuthBackend to AUTHENTICATION_BACKENDS

    AUTHENTICATION_BACKENDS = (
        'django.contrib.auth.backends.ModelBackend',
        'django_sharedauth.backends.SharedAuthBackend',
    )
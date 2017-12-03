import os
import os.path
import pwd

from .base import *  # pylint: disable=unused-wildcard-import,wildcard-import

# Run in debug mode.

DEBUG = True

TEMPLATES[0]['OPTIONS']['auto_reload'] = DEBUG
WHITENOISE_AUTOREFRESH = DEBUG

# Save media files to the user's Sites folder.

INSTALLED_APPS = [
    'whitenoise.runserver_nostatic',
] + INSTALLED_APPS

# INSTALLED_APPS += [
#     'debug_toolbar'
# ]
#
# MIDDLEWARE_CLASSES = [
#     'debug_toolbar.middleware.DebugToolbarMiddleware',
# ] + MIDDLEWARE_CLASSES
#
#
# def show_toolbar(request):
#     return True
#
# DEBUG_TOOLBAR_CONFIG = {
#     "SHOW_TOOLBAR_CALLBACK" : show_toolbar,
# }


# Use local server.

SITE_DOMAIN = 'localhost:8000'

ALLOWED_HOSTS = [
    # Django's defaults.
    '127.0.0.1',
    'localhost',
    '::1',
    # For compatibility with Browsersync.
    '0.0.0.0',
    'futily.dev',
]

PREPEND_WWW = False

# Optional separate database settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': 'localhost',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
    },
}

# Mailtrap SMTP
EMAIL_HOST = 'smtp.mailtrap.io'
EMAIL_HOST_USER = '94a4b4d4e3b0ee'
EMAIL_HOST_PASSWORD = '96c5a97f3f6cfa'
EMAIL_PORT = '2525'
EMAIL_USE_TLS = True

SESSION_COOKIE_SECURE = False

CACHES['default']['BACKEND'] = 'django.core.cache.backends.dummy.DummyCache'

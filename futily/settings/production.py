from .base import *  # pylint: disable=unused-wildcard-import,wildcard-import

DEBUG = False
TEMPLATE_DEBUG = DEBUG
CSRF_COOKIE_SECURE = True

MEDIA_ROOT = os.path.join(BASE_ROOT, '../futily_media')
STATIC_ROOT = os.path.join(BASE_ROOT, '../futily_static')

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

INSTALLED_APPS += [
    'opbeat.contrib.django',
]

OPBEAT = {
    'ORGANIZATION_ID': 'f6b78f2bdc4d44a79b2310477d02d3a7',
    'APP_ID': '3b5fe8a8af',
    'SECRET_TOKEN': 'c124cd945f999ccd4c33b558666a87e99ddc5635'
}

MIDDLEWARE_CLASSES = [
    'opbeat.contrib.django.middleware.OpbeatAPMMiddleware',
] + MIDDLEWARE_CLASSES

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'opbeat': {
            'level': 'WARNING',
            'class': 'opbeat.contrib.django.handlers.OpbeatHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'futily': {
            'level': 'WARNING',
            'handlers': ['opbeat'],
            'propagate': False,
        },
        # Log errors from the Opbeat module to the console (recommended)
        'opbeat.errors': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
    },
}

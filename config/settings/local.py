from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS += [
    'django_extensions',
]

INTERNAL_IPS = [
    '127.0.0.1',
    'localhost',
]

CORS_ALLOW_ALL_ORIGINS = True

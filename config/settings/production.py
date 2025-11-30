from .base import *
import dj_database_url
import os

DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = config(
    'ALLOWED_HOSTS',
    default='*',
    cast=lambda v: [s.strip() for s in v.split(',')]
)

# Database configuration with Supabase PostgreSQL
if config('DATABASE_URL', default=''):
    DATABASES['default'] = dj_database_url.config(
        default=config('DATABASE_URL'),
        conn_max_age=600,
        conn_health_checks=True,
        ssl_require=True,
    )
else:
    # Fallback to individual DB settings
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME', default='hishamos_db'),
        'USER': config('DB_USER', default='postgres'),
        'PASSWORD': config('DB_PASSWORD', default=''),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
        'OPTIONS': {
            'sslmode': 'require',
        }
    }

# Static files with WhiteNoise
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Security settings
SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=False, cast=bool)
SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default=True, cast=bool)
CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', default=True, cast=bool)
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_SECONDS = config('SECURE_HSTS_SECONDS', default=31536000, cast=int)
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
X_FRAME_OPTIONS = 'DENY'

# CORS for frontend
CORS_ALLOWED_ORIGINS = config(
    'CORS_ALLOWED_ORIGINS',
    default='',
    cast=lambda v: [s.strip() for s in v.split(',')] if v else []
)
CORS_ALLOW_ALL_ORIGINS = config('CORS_ALLOW_ALL_ORIGINS', default=False, cast=bool)

# Logging
LOGGING['handlers']['console']['level'] = 'INFO'
LOGGING['root'] = {
    'level': 'INFO',
    'handlers': ['console'],
}

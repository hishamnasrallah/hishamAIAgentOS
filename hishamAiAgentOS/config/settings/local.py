from .base import *

DEBUG = True
ALLOWED_HOSTS = ['*']

# Use SQLite for local dev if preferred, or override with Postgres in .env
# For now, we keep the base database config which defaults to sqlite3 if DB env vars aren't set,
# but let's make it explicit that we can override here.

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

"""
Django settings for it project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'SECURITY WARNING: keep the secret key used in production secret!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
TEMPLATE_DEBUG = False

ALLOWED_HOSTS = []

# Application definition



INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'dashboard',
    'ldap_login',
    'globaltags',
    'elmotor',
    'tasks',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)


ROOT_URLCONF = 'to.urls'

WSGI_APPLICATION = 'to.wsgi.application'

AUTHENTICATION_BACKENDS = ('to.backends.TasksBackend',)

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASE_ROUTERS = ["to.db_router.ProjectDbRouter"]
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'it',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    },
    'elmotor': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'elmotor',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    },
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = None

USE_I18N = True

USE_L10N = True

USE_TZ = False

#TEMPLATE_STRING_IF_INVALID = ""

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/


STATIC_ROOT =  os.path.join(BASE_DIR, 'static')
MEDIA_ROOT =  os.path.join(BASE_DIR, 'media')
STATIC_URL = '/to/static/'
MEDIA_URL = '/to/media/'

ADMIN_MEDIA_PREFIX = '/static/admin/'

TEMPLATE_DIRS = (
     os.path.join(BASE_DIR, 'templates'), 
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# load local settings
try:
    from local_settings import *
except ImportError:
    pass

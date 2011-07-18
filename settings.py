# Django settings for helsinki project.

import os.path
PROJECT_DIR = os.path.dirname(__file__)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = ( )

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_DIR, 'dev_data.sqlite'),
    },
    'nop': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_DIR, 'dev_nop.sqlite'),
    }
}

TIME_ZONE = 'Europe/Vienna'

LANGUAGE_CODE = 'de'

SITE_ID = 1

USE_I18N = True
USE_L10N = True

LOCALE_PATHS = os.path.join(PROJECT_DIR, 'locale')

MEDIA_ROOT = os.path.join(PROJECT_DIR, 'site_media')
MEDIA_URL = '/site_media/'

ADMIN_MEDIA_PREFIX = '/media/'

SECRET_KEY = ''

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_DIR, "templates"),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'program',
    'nop',
    'tinymce',
)

TINYMCE_DEFAULT_CONFIG = {
    'plugins' : 'contextmenu',
    'theme': 'advanced',
    'theme_advanced_toolbar_location': 'top',
}

try:
    from local_settings import *
except ImportError:
    pass

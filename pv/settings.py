# Django settings for pv project.

import os.path

PROJECT_DIR = os.path.dirname(__file__)

DEBUG = True

ADMINS = ()

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

DATABASE_ROUTERS = ['nop.dbrouter.NopRouter']

TIME_ZONE = 'Europe/Vienna'

LANGUAGE_CODE = 'de'

SITE_ID = 1

USE_I18N = True
USE_L10N = True

LOCALE_PATHS = (
    os.path.join(PROJECT_DIR, 'locale'),
)

MEDIA_ROOT = os.path.join(PROJECT_DIR, 'site_media')
MEDIA_URL = '/site_media/'

STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')
STATIC_URL = '/static/'

SECRET_KEY = ''

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT_DIR, 'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'pv.urls'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'program',
    'nop',
    'tinymce',
)

TINYMCE_JS_URL = '/static/js/tiny_mce/tiny_mce.js'
TINYMCE_DEFAULT_CONFIG = {
    'plugins': 'contextmenu',
    'theme': 'advanced',
    'theme_advanced_toolbar_location': 'top',
}

CACHE_BACKEND = 'locmem://'

MUSIKPROG_IDS = (
    1,    # unmodieriertes musikprogramm
)
SPECIAL_PROGRAM_IDS = ()

try:
    from local_settings import *
except ImportError:
    pass

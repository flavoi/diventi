# -*- coding: utf-8 -*-

"""
Django settings for diventi project.

Generated by 'django-admin startproject' using Django 1.11.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

from pathlib import Path
import os, sys, json

from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext_lazy as _


PROJ_ROOT = Path(__file__).resolve().parent.parent.parent 
BASE_DIR = PROJ_ROOT / 'diventi'

# JSON-based secrets module
with open(PROJ_ROOT / 'secrets.json', 'r') as f:
    secrets = json.load(f)

def get_env_variable(var_name):
    """Get the secret variable or return explicit exception."""
    try:
        return secrets[var_name]
    except KeyError:
        error_msg = "Set the {0} enviroment variable".format(settings)
        raise ImproperlyConfigured(error_msg)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',                
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'diventi.core.context.footer',
                'diventi.landing.context.feedback_form',
                'diventi.accounts.context.user_preferred_language',
            ],
        },
    },
    {
        'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'DIRS': [],
        'APP_DIRS': True,
    },
]


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = None

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = None

ALLOWED_HOSTS = []

LOGIN_REDIRECT_URL = '/'

# Application definition

TRANSLATION_APPS = [
    'modeltranslation',
]

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.sites',
]

LOCAL_APPS = [
    'diventi.core',
    'diventi.accounts',
    'diventi.blog',
    'diventi.landing',
    'diventi.comments',
    'diventi.products',
    'diventi.homebrew',
    'diventi.feedbacks',
]

THIRD_PARTY_APPS = [
    'ckeditor',
    'storages',
    'django_comments',
    'braces',
    'rest_framework',
    'cuser',
    'captcha',
    'star_ratings',
    'mptt',
    'boto',
    'letsencrypt',
    'django_tex',
]

INSTALLED_APPS = TRANSLATION_APPS + DJANGO_APPS + LOCAL_APPS + THIRD_PARTY_APPS

COMMENTS_APP = 'diventi.comments'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'cuser.middleware.CuserMiddleware', 
]

ROOT_URLCONF = 'config.urls'

WSGI_APPLICATION = 'config.wsgi.application'


# Diventi user model
AUTH_USER_MODEL = 'accounts.DiventiUser'
AUTHENTICATION_BACKENDS = ('diventi.accounts.backends.EmailBackend',)

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en'

LANGUAGES = [
  ('it', _('Italian')),
  ('en', _('English')),
]

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

TIME_ZONE = 'Europe/Rome'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Django sites
# https://docs.djangoproject.com/en/1.11/ref/contrib/sites/

SITE_ID = 1


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]


# Recaptcha config
# https://github.com/praekelt/django-recaptcha

NOCAPTCHA = True


# Ckeditor config
# https://github.com/django-ckeditor/django-ckeditor

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Custom',
        'height': 500,
        'toolbar_Custom': [
            ['Styles', 'Format', 'Bold', 'Italic', 'Underline', 'Strike', 'SpellChecker', 'Undo', 'Redo'],
            ['Link', 'Unlink', 'Anchor'],
            ['Image', 'Table', 'HorizontalRule'],
            ['TextColor', 'BGColor'],
            ['Smiley', 'SpecialChar'], ['Source'],
        ],
    },    
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'log/diventi.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': True,
        },
    },
}
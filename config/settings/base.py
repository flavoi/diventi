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
from django.urls import reverse_lazy

from machina import MACHINA_MAIN_TEMPLATE_DIR, MACHINA_MAIN_STATIC_DIR


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
        'DIRS': [
            BASE_DIR / 'templates',
            BASE_DIR / 'templates/machina',
            MACHINA_MAIN_TEMPLATE_DIR,
        ],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',                
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'machina.core.context_processors.metadata',
                'diventi.core.context.footer',
                'diventi.accounts.context.user_preferred_language',
                'diventi.accounts.context.user_statistics',
                'diventi.accounts.context.user_menu',
                'diventi.landing.context.graph_section',
                'diventi.landing.context.search_suggestions',
                'diventi.landing.context.about_us_articles',
                'diventi.products.context.project_categories',
                'diventi.products.context.pinned_projects',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ]
        },
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
LOGIN_URL = reverse_lazy('accounts:signin')

# Application definition

PREFIX_APPS = [
    'dal',
    'dal_select2',
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
    'diventi.feedbacks',
    'diventi.ebooks',
    'diventi.brave',
    'diventi.adventures',
    'diventi.tooltips',
    'diventi.payments',
]

THIRD_PARTY_APPS = [
    'ckeditor',
    'storages',
    'django_comments',
    'braces',
    'rest_framework',
    'captcha',
    'mptt',
    'boto',
    'letsencrypt',
    'reviews',
    'widget_tweaks',
    'haystack',
    'fullurl',
    'django_crontab',
#    'debug_toolbar',
]

FORUM_APPS = [
    'machina',
    'machina.apps.forum',
    'machina.apps.forum_conversation',
    'machina.apps.forum_conversation.forum_attachments',
    'machina.apps.forum_conversation.forum_polls',
    'machina.apps.forum_feeds',
    'machina.apps.forum_moderation',
    'machina.apps.forum_search',
    'machina.apps.forum_tracking',
    'machina.apps.forum_member',
    'machina.apps.forum_permission',
]

INSTALLED_APPS = PREFIX_APPS + DJANGO_APPS + LOCAL_APPS + THIRD_PARTY_APPS + FORUM_APPS

COMMENTS_APP = 'diventi.comments'

MIDDLEWARE = [
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'machina.apps.forum_permission.middleware.ForumPermissionMiddleware',
    'cuser.middleware.CuserMiddleware', 
]

ROOT_URLCONF = 'config.urls'

WSGI_APPLICATION = 'config.wsgi.application'

AUTH_USER_MODEL = 'accounts.DiventiUser'

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


# Cache config
# https://django-machina.readthedocs.io/en/stable/getting_started.html

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    },
    'machina_attachments': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': BASE_DIR / 'cache',
    },
}


# Recaptcha config
# https://github.com/praekelt/django-recaptcha

NOCAPTCHA = True


# Ckeditor config

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar_Basic': [
            ['Undo', 'Redo'],
            ['Styles', 'Format'],
            ['Link', 'Unlink', 'Anchor'],
            ['Image', 'Table', 'HorizontalRule', 'customEmbed'],
            ['Bold', 'Italic', 'Underline', 'Strike', 'RemoveFormat', 'TextColor', 'BGColor'],
            ['NumberedList', 'BulletedList', 'JustifyLeft', 'JustifyCenter', 'JustifyRight',],
            ['Source',],
        ],
        'toolbar': 'Basic',
        'extraPlugins': ','.join([
            'uploadimage', # the upload image feature
            # your extra plugins here
            'div',
            'autolink',
            'autoembed',
            'embedsemantic',
            'autogrow',
            # 'devtools',
            'widget',
            'lineutils',
            'clipboard',
            'dialog',
            'dialogui',
            'elementspath'
        ]),
        'stylesSet': [
            {
                "name": _('Base block'),
                "element": 'div',
                "styles": {
                    'padding': '5px 10px',
                    'background': '#eee',
                    'border': '1px solid #ccc',
                    'margin-bottom': '15px',
                }
            },
            {
                "name": _('Callout'),
                "element": 'div',
                "styles": {
                    'padding': '0.95rem',
                    'margin-top': '1.25rem',
                    'margin-bottom': '1.25rem',
                    'border-top': '1px solid #eee',
                    'border-bottom': '1px solid #eee',
                    'border-right': '1px solid #eee',
                    'border-left': '.25rem solid #fd7e14',
                }
            },
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


# Reviews config
# https://github.com/andreynovikov/django-rated-reviews

REVIEW_RATING_CHOICES = (
    ('1', _('Terrible')),
    ('2', _('Poor')),
    ('3', _('Average')),
    ('4', _('Very Good')),
    ('5', _('Excellent')),
)

REVIEW_PUBLISH_UNMODERATED = True


# Haystack config
# https://django-machina.readthedocs.io/en/stable/getting_started.html

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
    },
}


# Machina config
# https://django-machina.readthedocs.io/en/stable/settings.html

MACHINA_DEFAULT_AUTHENTICATED_USER_FORUM_PERMISSIONS = [
    'can_see_forum',
    'can_read_forum',
    'can_start_new_topics',
    'can_reply_to_topics',
    'can_edit_own_posts',
    'can_post_without_approval',
    'can_create_polls',
    'can_vote_in_polls',
    'can_download_file',
]

MACHINA_FORUM_NAME = 'Diventi'

MACHINA_USER_DISPLAY_NAME_METHOD = 'get_diventi_username'

MACHINA_PROFILE_AVATARS_ENABLED = False

MACHINA_MARKUP_LANGUAGE = None
MACHINA_MARKUP_WIDGET = 'ckeditor.widgets.CKEditorWidget'


# Stripe payments
# https://dashboard.stripe.com/test/apikeys

STRIPE_SECRET_KEY = get_env_variable('STRIPE_SECRET_KEY')
STRIPE_PUBLISHABLE_KEY = get_env_variable('STRIPE_PUBLISHABLE_KEY')
STRIPE_ENDPOINT_SECRET_KEY = get_env_variable('STRIPE_ENDPOINT_SECRET_KEY')


# Dropbox paper
# https://www.dropbox.com/developers/apps/info/xdrh4eoh3bpppnv

DROPBOX_ACCESS_TOKEN = get_env_variable('DROPBOX_ACCESS_TOKEN')
DIVENTI_UNIVERSALE_PAPER_ID = get_env_variable('DIVENTI_UNIVERSALE_PAPER_ID')
PRINT_HTML_EBOOK = False

# Email backend for testing and development
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

EMAIL_BACKEND = ''
EMAIL_HOST =  get_env_variable('EMAIL_HOST_KEY') # mail service smtp
EMAIL_HOST_USER = get_env_variable('EMAIL_HOST_USER_KEY') # email id
EMAIL_HOST_PASSWORD = get_env_variable('EMAIL_HOST_PASSWORD_KEY') # password
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# Django debug toolbar
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html
# print("IP Address for debug-toolbar: " + self.request.META['REMOTE_ADDR'])

INTERNAL_IPS = [
    '10.0.2.2',
]
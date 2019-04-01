# -*- coding: utf-8 -*-

import dj_database_url, os

from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_env_variable('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Forse https
SECURE_SSL_REDIRECT = True

# Host static and media on Amazon S3 support
# http://aws.amazon.com/

AWS_ACCESS_KEY_ID = get_env_variable('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = get_env_variable('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = get_env_variable('AWS_STORAGE_BUCKET_NAME')

AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

STATICFILES_LOCATION = 'static'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
STATICFILES_STORAGE = 'diventi.core.storages.StaticStorage'
STATIC_URL = '//%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, STATICFILES_LOCATION)

ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

MEDIAFILES_LOCATION = 'media'
MEDIA_ROOT = '/%s/' % MEDIAFILES_LOCATION
DEFAULT_FILE_STORAGE = 'diventi.core.storages.MediaStorage'
MEDIA_URL = '//%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, MEDIAFILES_LOCATION)


# Recaptcha config
# https://github.com/praekelt/django-recaptcha

RECAPTCHA_PUBLIC_KEY = get_env_variable('RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY = get_env_variable('RECAPTCHA_PRIVATE_KEY')


# Email backend for testing and development
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

EMAIL_HOST_KEY = get_env_variable('EMAIL_HOST_KEY')
EMAIL_HOST_USER_KEY = get_env_variable('EMAIL_HOST_USER_KEY')
EMAIL_HOST_PASSWORD_KEY = get_env_variable('EMAIL_HOST_PASSWORD_KEY')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = EMAIL_HOST_KEY # mail service smtp
EMAIL_HOST_USER = EMAIL_HOST_USER_KEY # email id
EMAIL_HOST_PASSWORD = EMAIL_HOST_PASSWORD_KEY # password
EMAIL_PORT = 587
EMAIL_USE_TLS = True
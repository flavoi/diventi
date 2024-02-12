# -*- coding: utf-8 -*-

from .base import *

import os

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 't##w+fo_&i#r89bj%_o4kq*m3e2i(02d7fp)yg!&&go^ie&=7o'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJ_ROOT, 'diventi.sqlite'),
    }
}

# Set short cache timeout
CACHE_TIMEOUT = 30

ALLOWED_HOSTS = [
    '192.168.1.96',
    '192.168.3.10',
    'localhost',
]

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
STATICFILES_STORAGE = 'diventi.core.storages.StaticStorage'
STATIC_URL = '//%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, STATICFILES_LOCATION)

ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

MEDIAFILES_LOCATION = 'dev/media'
MEDIA_ROOT = '/%s/' % MEDIAFILES_LOCATION
DEFAULT_FILE_STORAGE = 'diventi.core.storages.MediaStorage'

MEDIA_URL = '//%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, MEDIAFILES_LOCATION)

# Email backend for testing and development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Django cron jobs
# https://gutsytechster.wordpress.com/2019/06/24/how-to-setup-a-cron-job-in-django/
CRONJOBS = [
    (
        '*/1 * * * *', 
        'diventi.ebooks.cron.fetch_paper_books', 
        '--settings=config.settings.local >%s/log/cron.log' % BASE_DIR,
    ),
]
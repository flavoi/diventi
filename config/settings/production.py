import dj_database_url

from .base import *


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_env_variable('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    "default": dj_database_url.config(),
}

ALLOWED_HOSTS = [
    'diventi.herokuapp.com', 
    'localhost',
]


# Amazon S3 support
# http://aws.amazon.com/

STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3BotoStorage'

AWS_ACCESS_KEY_ID = get_env_variable('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = get_env_variable('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = get_env_variable('AWS_STORAGE_BUCKET_NAME')

AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_QUERYSTRING_AUTH = False
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

STATIC_S3_PATH = 'static'
DEFAULT_S3_PATH = 'media'

STATIC_URL = '//%s/' % AWS_S3_CUSTOM_DOMAIN
STATICFILES_DIRS = (BASE_DIR / 'static' / 'diventi',)
STATIC_ROOT = 'staticfiles'
MEDIA_URL = STATIC_URL + DEFAULT_S3_PATH
MEDIA_ROOT = '/%s/' % DEFAULT_S3_PATH
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'
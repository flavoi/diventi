from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 't##w+fo_&i#r89bj%_o4kq*m3e2i(02d7fp)yg!&&go^ie&=7o'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Database
# https://devcenter.heroku.com/articles/heroku-postgresql

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "diventi",
        "USER": "flavio",
        "PASSWORD": "",
        "HOST": "localhost",
        "PORT": "",
    }
}

# Set short cache timeout
CACHE_TIMEOUT = 30

ALLOWED_HOSTS = [
    '127.0.0.1', 
    'localhost'
]
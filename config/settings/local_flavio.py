from .local import *

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "diventi",
        "USER": "flavio",
        "PASSWORD": "flavio",
        "HOST": "localhost",
        "PORT": "",
    }
}
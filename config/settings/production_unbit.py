# -*- coding: utf-8 -*-

from .production import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': PROJ_ROOT / 'diventi.sqlite',
    }
}

ALLOWED_HOSTS = [
    'playdiventi.it', 
    'localhost',
]
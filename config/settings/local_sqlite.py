# -*- coding: utf-8 -*-

from .local import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': PROJ_ROOT / 'diventi.sqlite',
    }
}
# -*- coding: utf-8 -*-

from .production import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJ_ROOT, 'diventi.sqlite'),
    }
}
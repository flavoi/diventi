# -*- coding: utf-8 -*-
# Specific PythonAnywhere deployment

from .production import *

import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJ_ROOT, 'diventi.sqlite'),
    }
}

ALLOWED_HOSTS = [
    'playdiventi.it', 
    'localhost',
    'flaviomarcato.pythonanywhere.com',
]
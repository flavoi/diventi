# -*- coding: utf-8 -*-
# Specific PythonAnywhere deployment

from .production import *

import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': get_env_variable('DB_NAME'),
        'USER': get_env_variable('DB_USER'),
        'PASSWORD': get_env_variable('DB_PASSWORD'),
        'HOST': get_env_variable('DB_HOST'),
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        },
    }
}

ALLOWED_HOSTS = [
    'www.playdiventi.it', 
    'playdiventi.it', 
    'localhost',
    'flaviomarcato.pythonanywhere.com',
]
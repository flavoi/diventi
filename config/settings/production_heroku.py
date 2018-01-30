# -*- coding: utf-8 -*-
# Specific Heroku deployment

DATABASES = {
    "default": dj_database_url.config(),
}

ALLOWED_HOSTS = [
    'diventi.herokuapp.com', 
    'localhost',
]
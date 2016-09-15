"""
Development specific settings.
"""
from .base import *

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'pic',
        'USER': 'postgres',
        'PASSWORD': 'codango',
        'HOST': '0.0.0.0',
        'PORT': '5432'
    }
}

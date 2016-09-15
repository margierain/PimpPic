"""
Test specific settings.
"""

from .base import *

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
SECRET_KEY = os.getenv('SECRET_KEY')

NOSE_ARGS = [
    '--with-coverage',
    '--cover-package=api',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'testdb',
    }
}

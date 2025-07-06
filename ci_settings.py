
from FasterRunner.settings.base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

SECRET_KEY = 'test-secret-key-for-ci-only'
DEBUG = False
ALLOWED_HOSTS = ['*']
USE_LDAP = False


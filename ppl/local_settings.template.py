import os
from random import SystemRandom
import string

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = ''.join(
    SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in
    range(64))

DEBUG = False
ALLOWED_HOSTS = ['ppl.hackucf.org', '127.0.0.1']

ADMINS = (
    ('Mark Ignacio', 'mignacio@hackucf.org'),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

STATIC_ROOT = os.path.join(BASE_DIR, '_static')


SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = ''
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = ''

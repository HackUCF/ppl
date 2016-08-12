import os
import string
from random import SystemRandom

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = ''.join(SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(64))

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

SOCIAL_AUTH_GOOGLE_WHITELISTED_DOMAINS = ['hackucf.org']
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = ''
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = ''

# HTTPS settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Google settings
GOOGLE_APPLICATION_NAME = 'Hack@UCF Membership Updater v1'
GOOGLE_CLIENT_SECRET_FILE = os.path.join(BASE_DIR, 'client_secret.json')
GOOGLE_MEMBERSHIP_FILE_ID = '1Cj8HQ8fKarE_6L2dDmG6ilva5ziyF_rSx8YBqm8BKUI'
GOOGLE_RESUME_RESPONSES_FILE_ID = '13wOLalcADsOklo6klNC5lpVvGhDnqdtHJLzrV6o9gMQ'

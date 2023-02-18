import os

try:
    import local_settings
except ImportError:
    local_settings = None

DEBUG = getattr(local_settings, 'LOCAL_DEBUG', True)

ALLOWED_HOSTS = ['*']

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))

ROOT_URLCONF = 'urls'

SECRET_KEY = getattr(local_settings, 'LOCAL_SECRET_KEY', '')

STATIC_URL = '/static/'

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
    'index',
]


'''=======================USER_OPTION======================='''
MAIN_URL = 'http://iss.moex.com/iss'
REQUEST_RETURN_TYPE = 'json'

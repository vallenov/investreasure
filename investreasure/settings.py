import os

try:
    import local_settings
except ImportError:
    local_settings = None

DEBUG = getattr(local_settings, 'LOCAL_DEBUG', True)

ALLOWED_HOSTS = ['*']

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))

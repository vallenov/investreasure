try:
    import local_settings
except ImportError:
    local_settings = None

DEBUG = getattr(local_settings, 'LOCAL_DEBUG', True)

ALLOWED_HOSTS = ['*']

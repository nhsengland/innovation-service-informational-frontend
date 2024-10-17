from .base import *

DEBUG = False

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS').split(',') if os.environ.get('ALLOWED_HOSTS') else []
SESSION_COOKIE_SAMESITE = 'Strict'
SESSION_COOKIE_SECURE = True

# Static files
COMPRESS_OFFLINE = True

try:
    from .local import *
except ImportError:
    pass

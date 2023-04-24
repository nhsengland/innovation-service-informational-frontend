from .base import *

DEBUG = False

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS').split(',') if os.environ.get('ALLOWED_HOSTS') else []

# Static files
COMPRESS_OFFLINE = True

try:
    from .local import *
except ImportError:
    pass

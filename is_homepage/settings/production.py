from .base import *

DEBUG = False

ALLOWED_HOSTS = os.environ.get("DB_HOST").split(',')

try:
    from .local import *
except ImportError:
    pass

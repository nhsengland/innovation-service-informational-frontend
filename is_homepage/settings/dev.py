from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*']

# Debug toolbar config.
INSTALLED_APPS = INSTALLED_APPS + ['debug_toolbar']
MIDDLEWARE = MIDDLEWARE + ['debug_toolbar.middleware.DebugToolbarMiddleware']
INTERNAL_IPS = ('0.0.0.0', '127.0.0.1', '172.17.0.1')

USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

try:
    from .local import *
except ImportError:
    pass

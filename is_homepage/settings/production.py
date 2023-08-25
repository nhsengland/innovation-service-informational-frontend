from .base import *

DEBUG = False

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS').split(',') if os.environ.get('ALLOWED_HOSTS') else []

# Static files
COMPRESS_OFFLINE = True

# CSP policies.
# MIDDLEWARE = MIDDLEWARE + ['csp.middleware.CSPMiddleware']
MIDDLEWARE = MIDDLEWARE + ['is_homepage.config.middleware.CSPMiddleware']
# CSP_FRAME_SRC = ("'self'", "youtube.com", "https://www.youtube.com")


try:
    from .local import *
except ImportError:
    pass

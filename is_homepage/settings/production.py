from .base import *

DEBUG = False

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS").split(',') if os.environ.get("ALLOWED_HOSTS") else []

# Static files
STATICFILES_STORAGE = ('whitenoise.storage.CompressedManifestStaticFilesStorage')
INSTALLED_APPS += ["whitenoise.runserver_nostatic"]
MIDDLEWARE += ["whitenoise.middleware.WhiteNoiseMiddleware"]
    
try:
    from .local import *
except ImportError:
    pass

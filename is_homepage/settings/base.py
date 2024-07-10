"""
Django settings for is_homepage project.

Generated by 'django-admin startproject' using Django 4.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

import mimetypes
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/


# Application definition

INSTALLED_APPS = [
    "is_homepage.apps.base",
    "is_homepage.apps.base_navigation",
    "is_homepage.apps.base_scheduler",
    "is_homepage.apps.case_studies",
    "is_homepage.apps.contact_us",
    "is_homepage.apps.generic",
    "is_homepage.apps.generic_navigation",
    "is_homepage.apps.home",
    "is_homepage.apps.innovation_guides",
    "is_homepage.apps.news",
    "is_homepage.apps.search",
    "is_homepage.apps.help_resources",

    'compressor',
    'wagtailnhsukfrontend',
    'wagtailnhsukfrontend.forms',
    'wagtailmetadata',
    'wagtail_pdf_view',

    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    'wagtail.contrib.routable_page',
    "wagtail.contrib.search_promotions",
    'wagtail.contrib.settings',
    'wagtail.contrib.styleguide',
    "wagtail.contrib.typed_table_block",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    "wagtail",
    "modelcluster",
    "taggit",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.sitemaps",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "is_homepage.middleware.fetch_original_host.FetchOriginalHostMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
]

ROOT_URLCONF = "is_homepage.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(PROJECT_DIR, "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "wagtail.contrib.settings.context_processors.settings",

                'is_homepage.config.context_processors.environment.environment_variables'
            ]
        }
    }
]

WSGI_APPLICATION = "is_homepage.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': os.environ.get("DB_HOST"),
        'PORT': os.environ.get("DB_PORT"),
        'USER': os.environ.get("DB_USER"),
        'PASSWORD': os.environ.get("DB_PASSWORD"),
        'NAME': os.environ.get("DB_NAME")
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder"
]

STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, "static"),
]

# ManifestStaticFilesStorage is recommended in production, to prevent outdated
# JavaScript / CSS assets being served from cache (e.g. after a Wagtail upgrade).
# See https://docs.djangoproject.com/en/4.1/ref/contrib/staticfiles/#manifeststaticfilesstorage
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"

STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = "/static/"

MEDIA_ROOT = os.environ.get('MEDIA_PATH') or os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"


# Wagtail settings

WAGTAIL_SITE_NAME = "Innovation Service Homepage"

# Search
# https://docs.wagtail.org/en/stable/topics/search/backends.html

ES_API_URL = os.environ.get('ES_API_URL')
ES_API_KEY = os.environ.get('ES_API_KEY')

if (ES_API_URL):
    WAGTAILSEARCH_BACKENDS = {
        "default": {
            'BACKEND': 'is_homepage.apps.search.custom_elasticsearch8',
            'URLS': [ES_API_URL],
            'INDEX': 'wagtail',
            'TIMEOUT': 5,
            'OPTIONS': {
                'api_key': ES_API_KEY
            },
            'INDEX_SETTINGS': {
                'settings': {
                    'analysis': {
                        'analyzer': {
                            'default': {
                                'type': 'english',
                                'filter': ['stop']
                            }
                        }
                    }
                }
            },
        }
    }
else:
    WAGTAILSEARCH_BACKENDS = {
        "default": {
            'BACKEND': 'wagtail.search.backends.database',
        }
    }

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
WAGTAILADMIN_BASE_URL = "http://example.com"


# Custom settings.

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
CSRF_TRUSTED_ORIGINS = os.environ.get('CSRF_TRUSTED_ORIGINS').split(',') if os.environ.get('CSRF_TRUSTED_ORIGINS') else []

COMPRESS_PRECOMPILERS = [('text/x-scss', 'django_libsass.SassCompiler')]

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

FORM_RENDERER = 'wagtailnhsukfrontend.forms.renderers.NHSUKFrontendRenderer'

WAGTAILEMBEDS_RESPONSIVE_HTML = True

BASE_SCHEDULER_ENABLED = os.environ.get('SCHEDULER_DISABLE') != 'true'
BASE_SCHEDULER_MINUTE_TO_PUBLISH = os.environ.get('SCHEDULER_MINUTE_TO_PUBLISH', ':01')
BASE_SCHEDULER_MINUTE_TO_JOB_CLEANUP = os.environ.get('SCHEDULER_MINUTE_TO_CLEANUP', ':05')

if 'BASEURL' in os.environ:
    WEASYPRINT_BASEURL = os.environ.get('BASEURL')
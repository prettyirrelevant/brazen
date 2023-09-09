"""
Django settings for the brazen project.

Generated by 'django-admin startproject' using Django 4.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
from datetime import timedelta
from pathlib import Path
from typing import Any

from environ import Env
from huey import RedisHuey
from redis.connection import ConnectionPool

BASE_DIR = Path(__file__).resolve().parent.parent

env = Env()

# ==============================================================================
# CORE SETTINGS
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/
# ==============================================================================
DEBUG = env.bool('DEBUG', default=True)
if DEBUG:
    env.read_env(BASE_DIR / '.env.dev')

SECRET_KEY = env.str('SECRET_KEY')

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[]) if DEBUG else env.list('ALLOWED_HOSTS')

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'drf_yasg',
    'corsheaders',
    'django_filters',
    'rest_framework',
    'huey.contrib.djhuey',
    'rest_framework_simplejwt.token_blacklist',
]

LOCAL_APPS: list[str] = ['apps.accounts', 'apps.beneficiaries', 'apps.transactions', 'apps.disbursements']

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

WSGI_APPLICATION = 'brazen.wsgi.application'

ROOT_URLCONF = 'brazen.urls'

AUTH_USER_MODEL = 'accounts.Account'


# ==============================================================================
# MIDDLEWARE SETTINGS
# https://docs.djangoproject.com/en/4.2/topics/http/middleware/
# https://docs.djangoproject.com/en/4.2/ref/middleware/
# ==============================================================================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# ==============================================================================
# TEMPLATES SETTINGS
# ==============================================================================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# ==============================================================================
# DATABASES SETTINGS
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field
# ==============================================================================
DATABASES = {
    'default': env.db('DATABASE_URL'),
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ==============================================================================
# PASSWORD VALIDATION SETTINGS
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators
# ==============================================================================
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# ==============================================================================
# I18N AND L10N SETTINGS
# https://docs.djangoproject.com/en/4.2/topics/i18n/
# ==============================================================================
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# ==============================================================================
# STATIC FILES SETTINGS
# https://docs.djangoproject.com/en/4.2/howto/static-files/
# ==============================================================================
STATIC_URL = 'static/'

STATIC_ROOT = BASE_DIR / 'staticfiles'

STORAGES = {
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
    },
}


# ==============================================================================
# SECURITY
# ==============================================================================
SESSION_COOKIE_HTTPONLY = True

SESSION_COOKIE_SECURE = not DEBUG

CSRF_COOKIE_HTTPONLY = True

CSRF_COOKIE_SECURE = not DEBUG

SECURE_BROWSER_XSS_FILTER = True

X_FRAME_OPTIONS = 'DENY'


# ==============================================================================
# DJANGO REST FRAMEWORK SETTINGS
# ==============================================================================
REST_FRAMEWORK: dict[str, Any] = {
    'PAGE_SIZE': 20,
    'ORDERING_PARAM': 'order_by',
    'EXCEPTION_HANDLER': 'common.exception_handler.custom_exception_handler',
    'DEFAULT_RENDERER_CLASSES': ['rest_framework.renderers.JSONRenderer'],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.IsAuthenticatedOrReadOnly'],
    'DEFAULT_AUTHENTICATION_CLASSES': ['rest_framework_simplejwt.authentication.JWTAuthentication'],
}
if DEBUG:
    REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'].append('rest_framework.renderers.BrowsableAPIRenderer')


# ==============================================================================
# DJANGO CORS HEADERS SETTINGS
# ==============================================================================
CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',
    'https://brazen.vercel.app',
]

CORS_ALLOW_CREDENTIALS = True


# ==============================================================================
# HUEY SETTINGS
# ==============================================================================
connection_pool = ConnectionPool.from_url(env.str('HUEY_REDIS_URL'))
connection_pool.max_connections = env.int('HUEY_STORAGE_MAX_CONNECTIONS', default=5)

HUEY = RedisHuey(
    name=__name__,
    immediate=env.bool('HUEY_IMMEDIATE'),
    connection_pool=connection_pool,
)


# ==============================================================================
# LOGGING SETTINGS
# ==============================================================================
if not DEBUG:
    LOGGING = {
        'version': 1,
        'default_level': 'INFO',
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '[%(asctime)s] %(levelname)s:%(module)s:%(threadName)s:%(message)s',
            },
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose',
            },
        },
        'root': {'level': 'INFO', 'handlers': ['console']},
        'loggers': {
            'django.request': {
                'handlers': ['console'],
                'level': 'WARNING',
                'propagate': False,
            },
            'django.security.DisallowedHost': {
                'level': 'ERROR',
                'handlers': ['console'],
                'propagate': False,
            },
            'huey.consumer': {
                'level': 'INFO',
                'handlers': ['console'],
                'propagate': False,
            },
        },
    }


# ==============================================================================
# DRF-YASG SETTINGS
# ==============================================================================
SWAGGER_SETTINGS = {
    'USE_SESSION_AUTH': False,
    'SECURITY_DEFINITIONS': {
        'wallet_signature': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
        },
    },
}


# ==============================================================================
# RESEND MAIL SETTINGS
# ==============================================================================
RESEND_API_KEY = env.str('RESEND_API_KEY')


# ==============================================================================
# CACHE SETTINGS
# ==============================================================================
CACHES = {'default': env.cache()}


# ==============================================================================
# DJANGO REST FRAMEWORK SIMPLE-JWT SETTINGS
# ==============================================================================
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'UPDATE_LAST_LOGIN': True,
}

ANCHOR_BASE_URL = env.str('ANCHOR_BASE_URL')
ANCHOR_API_KEY = env.str('ANCHOR_API_KEY')

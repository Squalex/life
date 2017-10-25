"""
Django settings for life project.

Generated by 'django-admin startproject' using Django 1.11.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import dj_database_url
from bossoidc.settings import *

#########################################################
# Environment configuration
#########################################################
TRAVIS_ENVIRONMENT = False
HEROKU_ENVIRONMENT = False

if 'TRAVIS' in os.environ:
    TRAVIS_ENVIRONMENT = True
    DEBUG = False
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    ALLOWED_HOSTS = ['*']
elif 'HEROKU' in os.environ:
    HEROKU_ENVIRONMENT = True
    DEBUG = False
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    ALLOWED_HOSTS = ['*']
else:
    DEBUG = True
    ALLOWED_HOSTS = []


#########################################################
# Authentication
#########################################################

# Keycloak
# auth_uri = "http://localhost:8080/auth/realms/Life"
# client_id = "Life"
# public_uri = "http://localhost:8000"
# configure_oidc(auth_uri, client_id, public_uri)
from django.conf.global_settings import DATABASES

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    # 'bossoidc.backend.OpenIdConnectBackend',
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'oidc_auth.authentication.BearerTokenAuthentication',
    ),
}

#########################################################
# Base
#########################################################

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'jou8pt^m-on)^wtl-l7nuex7gq+bd87tm8(pprb12e^o9jlh^&'

# SECURITY WARNING: don't run with debug turned on in production!

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'bossoidc',
    # 'djangooidc',
    'core',
    'poker',
    'runtastic',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'life.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # 'social_django.context_processors.backends',
                # 'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'life.wsgi.application'


#########################################################
# Database
#########################################################

# Update database configuration with $DATABASE_URL.
if TRAVIS_ENVIRONMENT:
    DATABASES = {
        'default': {
            'ENGINE':   'django.db.backends.postgresql_psycopg2',
            'NAME':     'travisdb',
            'USER':     'postgres',
            'PASSWORD': '',
            'HOST':     'localhost',
            'PORT':     '',
        }
    }
elif HEROKU_ENVIRONMENT:
    db_from_env = dj_database_url.config(conn_max_age=500)
    DATABASES['default'].update(db_from_env)
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'localbdd',
        }
    }

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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


#########################################################
# Internationalization
#########################################################

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


#########################################################
# Static files
#########################################################
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'


#########################################################
# Sentry
#########################################################
SENTRY_DSN = os.environ.get('SENTRY_DSN')
if SENTRY_DSN:
    INSTALLED_APPS += (
        'raven.contrib.django.raven_compat',
    )
    RAVEN_CONFIG = {
        'dsn': SENTRY_DSN,
        'release': os.environ.get('HEROKU_SLUG_COMMIT', ''),
    }
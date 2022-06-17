"""
Django settings for django_excel project.

Generated by 'django-admin startproject' using Django 4.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""


import os
from pathlib import Path
from typing import Any

from celery.schedules import crontab
from decouple import Csv, config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY: str = config('SECRET_KEY', default='django-insecure-i)%z*h8v&tkx946m#3_!+48ao#7xea7dy3jql$c_&r(6x)vudo')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG: bool = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS: list[str] = config('ALLOWED_HOSTS', default='127.0.0.1,localhost', cast=Csv())


# Application definition

INSTALLED_APPS: list[str] = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core.apps.CoreConfig',
]

MIDDLEWARE: list[str] = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF: str = 'django_excel.urls'

TEMPLATES: list[dict[str, Any]] = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION: str = 'django_excel.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES: dict[str, Any] = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

if os.environ.get('GITHUB_WORKFLOW'):
    DATABASES['default']['ENGINE'] = 'django.db.backends.postgresql_psycopg2'
    DATABASES['default']['NAME'] = 'github_actions'
    DATABASES['default']['USER'] = 'postgres'
    DATABASES['default']['PASSWORD'] = 'postgres'
    DATABASES['default']['HOST'] = '127.0.0.1'
    DATABASES['default']['PORT'] = 5432


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS: list[dict[str, str]] = [
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


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE: str = 'en-us'

TIME_ZONE: str = 'UTC'

USE_I18N: bool = True

USE_TZ: bool = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL: str = 'static/'
STATIC_ROOT: str = BASE_DIR / 'staticfiles'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD: str = 'django.db.models.BigAutoField'


CELERY_BROKER_URL: str = config('REDIS_URL', default='amqp://localhost')
CELERY_RESULT_BACKEND: str = config('REDIS_URL', default='')
CELERY_ACCEPT_CONTENT: list[str] = ['application/json']
CELERY_TASK_SERIALIZER: str = 'json'
CELERY_RESULT_SERIALIZER: str = 'json'
CELERY_BEAT_SCHEDULE: dict[str, dict[str, Any]] = {
    'get_coins_data_from_coingecko_and_store': {
        'task': 'core.tasks.get_coins_data_from_coingecko_and_store',
        'schedule': crontab(minute='*/1'),
    },
    'populate_googlesheet_with_coins_data': {
        'task': 'core.tasks.populate_googlesheet_with_coins_data',
        'schedule': crontab(minute='*/2'),
    },
}


CELERY_ALWAYS_EAGER = True
CELERY_EAGER_PROPAGATES = True
BROKER_BACKEND = 'memory'

# Google API Configurations
GOOGLE_API_SCOPE = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = config('SPREADSHEET_ID', default='1AFNyUKcqgwO-CCXRubcIALOC74yfV716Q5q57Ojjicc')
GOOGLE_API_SERVICE_KEY_URL = config('SERVICE_KEY_PATH', default='')
SPREADSHEET_TAB_EXPIRY = config('SPREADSHEET_TAB_EXPIRY', default=360, cast=int)

# Email configuration
ADMINS = (('Admin', config('EMAIL_HOST_USER', default='no-reply@django_excel.herokuapp.com')),)
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')

if not DEBUG:
    import dj_database_url

    # ==============================================================================
    # SECURITY SETTINGS
    # ==============================================================================

    CSRF_COOKIE_SECURE = True
    CSRF_COOKIE_HTTPONLY = True

    SECURE_HSTS_SECONDS = 60 * 60 * 24 * 7 * 52  # one year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_SSL_REDIRECT = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

    SESSION_COOKIE_SECURE = True

    db_from_env = dj_database_url.config(conn_max_age=500)
    DATABASES['default'].update(db_from_env)

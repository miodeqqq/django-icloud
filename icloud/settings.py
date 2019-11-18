# -*- coding: utf-8 -*-

import datetime
import os
import sys

import dj_database_url
import pytz
from celery.schedules import crontab

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = False

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['*']

ADMINS = (
    ('miodeq', 'maciek@mjanuszewski.pl'),
)

MANAGERS = ADMINS

SITE_ID = 1

DEFAULT_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles'
)

PROJECT_APPS = (
    'core',
)

THIRD_PARTY_APPS = (
    'suit',
    'django.contrib.admin',
    'solo'
)

INSTALLED_APPS = DEFAULT_APPS + PROJECT_APPS + THIRD_PARTY_APPS

MIDDLEWARE = (
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.gzip.GZipMiddleware'
)

ROOT_URLCONF = 'icloud.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'icloud.wsgi.application'

DATABASE_URL = 'postgres://{user}:{password}@postgres:{db_port}/{db_name}'.format(
    user=os.environ.get('USER'),
    password=os.environ.get('PASSWORD'),
    db_name=os.environ.get('DB_NAME'),
    db_port=os.environ.get('DB_PORT')
)

DATABASES = {
    'default': dj_database_url.config(default=DATABASE_URL, conn_max_age=600)
}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True
USE_L10N = True
USE_TZ = True

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

if not os.path.exists(MEDIA_ROOT):
    os.mkdir(MEDIA_ROOT)

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

if not os.path.exists(STATIC_ROOT):
    os.mkdir(STATIC_ROOT)

LOG_ROOT = os.path.join(BASE_DIR, 'logs')

if not os.path.exists(LOG_ROOT):
    os.mkdir(LOG_ROOT)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

SUIT_CONFIG = {
    'ADMIN_NAME': u'iCloud manager v1.0',

    'MENU': (
        '-',
        {'app': 'core', 'label': u'iCloud config', 'icon': 'icon-home', 'models': (
            'userauthentication',
            'googlemapsapikey',
        )},
        '-',
        {'app': 'core', 'label': u'iCloud stats', 'icon': 'icon-list', 'models': (
            'iphonestatus',
            'icloudcontact',
            'icloudcalendar',
            'iphonelastknownlocation',
            'userdevices',
            'sendmessagetoiphone',
        )},
        '-',
        {'app': 'core', 'label': u'Errors', 'icon': 'icon-heart', 'models': (
            'exceptionstorage',
        )},
    ),
}

CELERY_IMPORTS = (
    'core.tasks',
)

REDIS_HOST = 'redis'

REDIS_PORT = 6379

REDIS_URL = "redis://{host}:{port}/".format(
    host=REDIS_HOST,
    port=REDIS_PORT
)

CELERY_BROKER_URL = REDIS_URL

CELERY_IGNORE_RESULT = True
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ALWAYS_EAGER = False
CELERY_ACKS_LATE = True
CELERY_TASK_PUBLISH_RETRY = True
CELERY_DISABLE_RATE_LIMITS = False
CELERY_MESSAGE_COMPRESSION = "gzip"
CELERYD_POOL_RESTARTS = True

CELERY_TIMEZONE = 'Europe/Warsaw'

CELERYD_PREFETCH_MULTIPLIER = 1
CELERYD_MAX_TASKS_PER_CHILD = 4
CELERY_TASK_RESULT_EXPIRES = 600
CELERYD_HIJACK_ROOT_LOGGER = False
CELERYD_CONCURRENCY = 16

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"

SESSION_CACHE_ALIAS = "default"

task_time_utc = lambda: datetime.datetime.now(pytz.timezone('UTC'))

# Celery
CELERYBEAT_SCHEDULE = {
    # get_user_devices_task
    'get_user_devices_task': {
        'task': 'get_user_devices_task',
        'schedule': crontab(minute=0, hour='*/8', nowfun=task_time_utc)
    },
    # get_user_iphone_status_task
    'get_user_iphone_status_task': {
        'task': 'get_user_iphone_status_task',
        'schedule': crontab(minute='*/15', nowfun=task_time_utc)
    },
    # get_user_iphone_location_task
    'get_user_iphone_location_task': {
        'task': 'get_user_iphone_location_task',
        'schedule': crontab(minute='*/5', nowfun=task_time_utc)
    },
    # get_user_contacts_task
    'get_user_contacts_task': {
        'task': 'get_user_contacts_task',
        'schedule': crontab(minute=0, hour='*/4', nowfun=task_time_utc)
    },
    # get_user_calendar_events_task
    'get_user_calendar_events_task': {
        'task': 'get_user_calendar_events_task',
        'schedule': crontab(minute=0, hour='*/1', nowfun=task_time_utc)
    },
}
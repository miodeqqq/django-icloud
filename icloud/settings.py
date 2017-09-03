# -*- coding: utf-8 -*-

import datetime
import os
import sys

import pytz
from celery.schedules import crontab

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = '380)8^^^*z*)24bf)!mc&%qt@@11dl7=^+=rb*+rj=&(h4^6*v'

DEBUG = False

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
    'django.contrib.staticfiles',
)

PROJECT_APPS = (
    'djcelery',
    'core',
)

THIRD_PARTY_APPS = (
    'suit',
    'django.contrib.admin',
    'solo',
)

INSTALLED_APPS = DEFAULT_APPS + PROJECT_APPS + THIRD_PARTY_APPS

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
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

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'HOST': 'postgres',
    }
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

CELERY_IMPORTS = [
    'core.tasks',
]

CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_MESSAGE_COMPRESSION = "gzip"

CELERY_ALWAYS_EAGER = False
CELERY_ACKS_LATE = True
CELERY_TASK_PUBLISH_RETRY = True
CELERY_DISABLE_RATE_LIMITS = False
CELERYD_POOL_RESTARTS = True

# Rabbitmq
RABBIT_HOSTNAME = 'rabbitmq'
BROKER_CONNECTION_TIMEOUT = 30
BROKER_POOL_LIMIT = 1
BROKER_URL = 'amqp://{user}:{password}@{hostname}/{vhost}/'.format(
    user='guest',
    password='guest',
    hostname=RABBIT_HOSTNAME,
    vhost=''
)

BROKER_TRANSPORT_OPTIONS = {'confirm_publish': True}

BROKER_HEARTBEAT = 30
BROKER_URL += '?heartbeat={heartbeat}'.format(heartbeat=BROKER_HEARTBEAT)

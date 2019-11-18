# -*- coding: utf-8 -*-

from __future__ import absolute_import

import os

import celery
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'icloud.settings')
django.setup()


class Celery(celery.Celery):
    """
    Celery class was overridden because we wanna support Sentry issues monitoring for Celery tasks
    """

    def on_configure(self):
        if hasattr(settings, 'RAVEN_CONFIG') and settings.RAVEN_CONFIG.get('dsn', None):
            import raven
            from raven.contrib.celery import register_signal, register_logger_signal

            client = raven.Client(settings.RAVEN_CONFIG['dsn'])
            register_logger_signal(client)
            register_signal(client)


app = Celery('icloud', broker_pool_limit=1, broker=settings.CELERY_BROKER_URL, result_backend=settings.REDIS_URL)

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

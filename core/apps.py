# -*- coding: utf-8 -*-

from django.apps import AppConfig


class CoreConfig(AppConfig):
    """
    Config label for core app (in Django Admin interface).
    """

    name = 'core'
    verbose_name = str('iCloud devices manager')
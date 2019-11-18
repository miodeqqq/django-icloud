# -*- coding: utf-8 -*-

import os

from django.core.management import BaseCommand

from core.models import UserAuthentication, GoogleMapsAPIKey


class Command(BaseCommand):
    """
    External manage.py command

    Example of usage:
        ./manage.py initial_data
    """

    help = 'Creates initial data for models.'

    def handle(self, *args, **options):
        """
        Override BaseCommand handle method.
        """

        # iCloud user
        user = UserAuthentication.get_solo()

        user.email = os.environ.get('ICLOUD_USER')
        user.password = os.environ.get('ICLOUD_PASSWORD')
        user.save()

        # Google Maps Static API key
        gm = GoogleMapsAPIKey.get_solo()

        gm.api_key = os.environ.get('GOOGLE_MAPS_API_KEY')
        gm.save()

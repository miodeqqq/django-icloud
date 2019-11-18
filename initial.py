# -*- coding: utf-8 -*-

import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "icloud.settings")
django.setup()

from core.models import UserAuthentication, GoogleMapsAPIKey


def create_icloud_user_and_gm_api_key():
    """
    Initial script for creating iCloud user and Google Maps Static API Key.
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


create_icloud_user_and_gm_api_key()

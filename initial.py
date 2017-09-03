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

    data = {}

    config_file = './config.txt'

    if os.path.exists(config_file):
        try:
            with open(config_file, 'r') as f:
                for line in f:
                    key, val = line.strip().split()
                    data[key] = val
        except IOError:
            print('No such file!')
            return 0

    # iCloud user
    user = UserAuthentication.get_solo()

    user.email = data.get('icloud_user')
    user.password = data.get('icloud_password')
    user.save()

    # Google Maps Static API key
    gm = GoogleMapsAPIKey.get_solo()

    gm.api_key = data.get('gm_api_key')
    gm.save()


create_icloud_user_and_gm_api_key()

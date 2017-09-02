# -*- coding: utf-8 -*-

from django.core.exceptions import ObjectDoesNotExist
from pyicloud import PyiCloudService

from core.models import UserAuthentication


def get_icloud_api_object():
    """
    General method to sign in and return iCloud API object.
    """

    try:
        user = UserAuthentication.get_solo()

        email = user.email
        password = user.password

        api = PyiCloudService(email, password)

        return api

    except ObjectDoesNotExist:
        pass


def get_user_devices(api_object):
    """
    Returns user's devices.
    """

    try:
        return api_object.devices
    except ObjectDoesNotExist:
        pass


def get_user_iphone(api_object):
    """
    Returns user's iPhone info (first device associated with the account).
    """
    try:
        return api_object.iphone
    except ObjectDoesNotExist:
        pass


def get_user_iphone_location(api_object):
    """
    Returns user's last known location.
    """

    try:
        return api_object.iphone.location()
    except ObjectDoesNotExist:
        pass


def get_user_iphone_status(api_object):
    """
    Returns user's iPhone properties.
    """
    try:
        return api_object.iphone.status()
    except ObjectDoesNotExist:
        pass


def play_user_iphone_sound(api_object):
    """
    Makes a request to iPhone to play a sound.
    """
    try:
        return api_object.iphone.play_sound()
    except ObjectDoesNotExist:
        pass


def send_message_to_iphone(api_object, phone_number, message):
    """
    Makes a request to iPhone: turns on the lost mode and display message on screen.
    """

    try:
        return api_object.iphone.lost_device(phone_number, message)
    except ObjectDoesNotExist:
        pass


def get_found_location_name(latitude, longitude):
    """
    Returns found location name with given coordinates.
    """

    from geopy.geocoders import Nominatim
    geolocator = Nominatim()

    location = geolocator.reverse("{latitude}, {longitude}".format(
        latitude=latitude,
        longitude=longitude
    ))

    return location.address

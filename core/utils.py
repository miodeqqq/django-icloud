# -*- coding: utf-8 -*-

from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from pyicloud import PyiCloudService
from requests import RequestException

from core.models import UserAuthentication


def get_icloud_api_object():
    """
    General method to sign in and return iCloud API object.
    """

    try:
        user = UserAuthentication.get_solo()

        email = user.email
        password = user.password

        return PyiCloudService(email, password)

    except (ObjectDoesNotExist, RequestException):
        pass


def get_user_devices(api_object):
    """
    Returns user's devices.
    """

    try:
        return api_object.devices
    except (ObjectDoesNotExist, RequestException):
        pass


def get_user_iphone(api_object):
    """
    Returns user's iPhone info (first device associated with the account).
    """
    try:
        return api_object.iphone
    except (ObjectDoesNotExist, RequestException):
        pass


def get_user_iphone_location(api_object):
    """
    Returns user's last known location.
    """

    try:
        return api_object.iphone.location()
    except (ObjectDoesNotExist, RequestException):
        pass


def get_user_iphone_status(api_object):
    """
    Returns user's iPhone properties.
    """
    try:
        return api_object.iphone.status()
    except (ObjectDoesNotExist, RequestException):
        pass


def play_user_iphone_sound(api_object):
    """
    Makes a request to iPhone to play a sound.
    """
    try:
        return api_object.iphone.play_sound()
    except (ObjectDoesNotExist, RequestException):
        pass


def send_message_to_iphone(api_object, phone_number, message):
    """
    Makes a request to iPhone: turns on the lost mode and display message on screen.
    """

    try:
        return api_object.iphone.lost_device(phone_number, message)
    except (ObjectDoesNotExist, RequestException):
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

    return location.address.strip()


def get_user_contacts(api_object):
    """
    Returns all iCloud user's contacts.
    """

    try:
        return api_object.contacts.all()
    except (ObjectDoesNotExist, RequestException):
        pass


def get_user_contacts_data(contacts_objects):
    """
    Returns single contact data.
    """

    contacts_data = []

    try:
        for contact in contacts_objects:
            contact_id = contact.get('contactId', None)
            first_name = contact.get('firstName', None)
            middle_name = contact.get('middleName', None)
            last_name = contact.get('lastName', None)
            photo_url = contact.get('photo', {}).get('url', None)
            etag = contact.get('etag', None)
            is_company = contact.get('isCompany', False)
            normalized = contact.get('normalized', None)
            phones = contact.get('phones', None)

            phone_number = None
            phone_label = None

            if phones and len(phones) == 1:
                phone_number = phones[0].get('field', None)
            if phones and len(phones) == 2:
                phone_number = phones[0].get('field', None)
                phone_label = phones[1].get('label', None)

            prefix = contact.get('prefix', None)
            suffix = contact.get('suffix', None)

            single_contact = contact_id, first_name, middle_name, last_name, photo_url, etag, is_company, normalized, phone_number, phone_label, prefix, suffix
            contacts_data.append(single_contact)

        return contacts_data

    except (ObjectDoesNotExist, RequestException):
        pass

    return []


def get_user_calendar_events(api_object):
    """
    Returns all iCloud user's calendar events.
    """

    try:
        return api_object.calendar.events()
    except (ObjectDoesNotExist, RequestException):
        pass


def get_proper_calendar_date(date_list):
    """
    Converts list of date strings into datetime object.
    """

    date_list.pop(0)
    date_list.pop(-1)
    datetime_obj = ' '.join(str(x) for x in date_list)

    return datetime.strptime(datetime_obj, '%Y %m %d %I %M')


def get_user_calendar_events_data(calendar_objects):
    """
    Returns single calendar object data.
    """

    calendar_data = []

    try:
        for calendar_item in calendar_objects:
            start_date = calendar_item.get('startDate', None)
            end_date = calendar_item.get('endDate', None)
            local_start_date = calendar_item.get('localStartDate', None)
            local_end_date = calendar_item.get('localEndDate', None)
            title = calendar_item.get('title', None)
            tz = calendar_item.get('tz', None)
            is_all_day = calendar_item.get('allDay', None)
            duration = calendar_item.get('duration', None)
            p_guid = calendar_item.get('pGuid', None)

            start_date = get_proper_calendar_date(start_date)
            end_date = get_proper_calendar_date(end_date)
            local_start_date = get_proper_calendar_date(local_start_date)
            local_end_date = get_proper_calendar_date(local_end_date)

            single_event = start_date, end_date, local_start_date, local_end_date, title, tz, is_all_day, duration, p_guid
            calendar_data.append(single_event)

        return calendar_data

    except (ObjectDoesNotExist, RequestException):
        pass

    return []

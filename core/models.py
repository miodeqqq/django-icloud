# -*- coding: utf-8 -*-

import logging

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from solo.models import SingletonModel

logger = logging.getLogger(__name__)


class GoogleMapsAPIKey(SingletonModel):
    """
    Stores API key for Google Maps.
    """

    api_key = models.CharField(
        'API key',
        max_length=255,
        blank=False,
        db_index=True
    )

    def __str__(self):
        return self.api_key

    class Meta:
        verbose_name = 'Google Maps API key'

class UserAuthentication(SingletonModel):
    """
    Stores user's username and password.
    """

    email = models.EmailField(
        'Username',
        max_length=255,
        db_index=True,
        blank=False
    )

    password = models.CharField(
        'Password',
        max_length=255,
        db_index=True,
        blank=False
    )

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'User\'s authentication'


class iPhoneStatus(SingletonModel):
    """
    Stores user's iPhone status info.
    """

    iphone_name = models.CharField(
        'Device name',
        blank=True,
        db_index=True,
        max_length=255
    )

    device_display_name = models.CharField(
        'Device display name',
        blank=True,
        db_index=True,
        max_length=255
    )

    battery_level = models.FloatField(
        'Battery level',
        db_index=True,
        blank=True,
        null=True
    )

    device_status = models.CharField(
        'Device status',
        max_length=255,
        db_index=True,
        blank=True
    )

    def __str__(self):
        return self.device_display_name

    class Meta:
        verbose_name = 'iPhone device status'


class iPhoneLastKnownLocation(models.Model):
    """
    Stores info about iPhone's last know location.
    """

    position_type = models.CharField(
        'Position type',
        blank=True,
        max_length=255,
        db_index=True
    )

    altitude = models.FloatField(
        'Altitude',
        blank=True,
        null=True,
        db_index=True
    )

    latitude = models.FloatField(
        'Latitude',
        blank=True,
        null=True,
        db_index=True
    )

    longitude = models.FloatField(
        'Longitude',
        blank=True,
        null=True,
        db_index=True
    )

    floor_level = models.PositiveSmallIntegerField(
        'Floor level',
        blank=True,
        default=0,
        db_index=True
    )

    horizontal_accuracy = models.FloatField(
        'Horizontal accuracy',
        blank=True,
        null=True,
        db_index=True
    )

    is_inaccurate = models.BooleanField(
        'Is inaccurate ?',
        default=False,
    )

    is_old = models.BooleanField(
        'Is old ?',
        default=False,
        db_index=True
    )

    location_finished = models.BooleanField(
        'Location finished',
        default=False,
        db_index=True
    )

    location_type = models.CharField(
        'Location type',
        max_length=255,
        blank=True,
        db_index=True,
    )

    vertical_accuracy = models.FloatField(
        'Vertical accuracy',
        blank=True,
        null=True,
        db_index=True,
    )

    timestamp = models.DateTimeField(
        'Timestamp',
        db_index=True,
        editable=False
    )

    found_location_name = models.TextField(
        'Location',
        db_index=True,
        blank=True
    )

    def __str__(self):
        return self.found_location_name if self.found_location_name else 'Unknown'

    class Meta:
        verbose_name = 'iPhone\'s last known location'
        verbose_name_plural = 'iPhone\'s last known locations'


class UserDevices(models.Model):
    """
    Stores user's devices info.
    """

    device_name = models.CharField(
        'Device',
        blank=True,
        max_length=255
    )

    def __str__(self):
        return self.device_name

    class Meta:
        verbose_name = 'User device'
        verbose_name_plural = 'User\'s devices'


class SendMessageToiPhone(models.Model):
    """
    Class for storing messages sent to iPhone (lost mode purposes).
    """

    phone_number = models.CharField(
        'Phone number',
        max_length=255,
        blank=False,
    )

    message = models.CharField(
        'Message',
        max_length=255,
        blank=False
    )

    status = models.BooleanField(
        'Sending status',
        default=False,
        db_index=True
    )

    timestamp = models.DateTimeField(
        'Date',
        auto_now_add=True,
        db_index=True,
        editable=False
    )

    def __str__(self):
        return self.phone_number

    class Meta:
        verbose_name = 'iPhone lost mode message'
        verbose_name_plural = 'iPhone lost mode messages'


@receiver(post_save, sender=SendMessageToiPhone, dispatch_uid='send_message_to_iphone')
def send_message_to_iphone(sender, instance, **kwargs):
    """
    Post save action to send message to iPhone(lost mode action).
    """

    from core.utils import send_message_to_iphone, get_icloud_api_object

    api = get_icloud_api_object()

    phone_number = instance.phone_number
    message = instance.message

    try:
        send_message_to_iphone(api, phone_number, message)
        instance.status = True
        instance.save()
    except Exception as exc:
        logger.info('[Sending message to iPhone] Error --> {exc}'.format(exc=exc))

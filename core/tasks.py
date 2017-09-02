# -*- coding: utf-8 -*-

import logging

from celery import shared_task

from core.utils import get_icloud_api_object

logger = logging.getLogger(__name__)


def backoff(attempts):
    """
    Returns a backoff delay, in seconds, given a number of attempts.

    The delay increases very rapidly with the number of attemps:
    1, 2, 4, 8, 16, 32, ...
    """

    return 2 ** attempts


@shared_task(
    name='get_user_devices_task',
    queue='update_icloud_data',
    max_retries=10,
    bind=True,
)
def get_user_devices_task(self):
    """
    Celery task to call iCloud API and retrieve user's data info.
    """

    from core.models import UserDevices
    from core.utils import get_user_devices

    api = get_icloud_api_object()
    get_user_data = get_user_devices(api)

    user_devices = [x for x in get_user_data]

    try:
        for user_device in user_devices:
            UserDevices.objects.get_or_create(
                device_name=user_device
            )
    except Exception as exc:
        logging.info('[Get user devices task] Error --> {exc}'.format(exc=exc))

        self.retry(
            countdown=backoff(self.request.retries),
            exc=exc
        )


@shared_task(
    name='get_user_iphone_status_task',
    queue='update_icloud_data',
    max_retries=10,
    bind=True,
)
def get_user_iphone_status_task(self):
    """
    Celery task to call iCloud API and retrieve iPhone's data info.
    """

    from core.models import iPhoneStatus
    from core.utils import get_user_iphone_status

    api = get_icloud_api_object()
    get_user_iphone_info = get_user_iphone_status(api)

    device_display_name = get_user_iphone_info.get('deviceDisplayName')
    device_status = get_user_iphone_info.get('deviceStatus')
    device_battery_level = get_user_iphone_info.get('batteryLevel')
    device_name = get_user_iphone_info.get('name')

    try:
        iphone = iPhoneStatus.get_solo()
        iphone.iphone_name=device_name
        iphone.device_display_name=device_display_name
        iphone.battery_level=device_battery_level
        iphone.device_status=device_status
        iphone.save()

    except Exception as exc:
        logging.info('[iPhone status task] Error --> {exc}'.format(exc=exc))

        self.retry(
            countdown=backoff(self.request.retries),
            exc=exc
        )


@shared_task(
    name='get_user_iphone_location_task',
    queue='update_icloud_data',
    max_retries=10,
    bind=True,
)
def get_user_iphone_location_task(self):
    """
    Celery task to call iCloud API and retrieve iPhone's last known location data.
    """

    from core.models import iPhoneLastKnownLocation
    from datetime import datetime
    from core.utils import get_user_iphone_location, get_found_location_name

    api = get_icloud_api_object()
    get_user_iphone_info = get_user_iphone_location(api)

    position_type = get_user_iphone_info.get('positionType')
    altitude = get_user_iphone_info.get('altitude')
    latitude = get_user_iphone_info.get('latitude')
    longitude = get_user_iphone_info.get('longitude')
    floor_level = get_user_iphone_info.get('floorLevel')
    horizontal_accuracy = get_user_iphone_info.get('horizontalAccuracy')
    is_inaccurate = get_user_iphone_info.get('isInaccurate')
    is_old = get_user_iphone_info.get('isOld')
    location_finished = get_user_iphone_info.get('locationFinished')
    location_type = get_user_iphone_info.get('locationType')
    vertical_accuracy = get_user_iphone_info.get('verticalAccuracy')
    timestamp = get_user_iphone_info.get('timeStamp')

    t_date = datetime.fromtimestamp(int(timestamp) / 1000.0)

    found_location_name = get_found_location_name(latitude, longitude)

    try:
        iPhoneLastKnownLocation.objects.get_or_create(
            position_type=position_type,
            altitude=altitude,
            latitude=latitude,
            longitude=longitude,
            floor_level=floor_level,
            horizontal_accuracy=horizontal_accuracy,
            is_inaccurate=is_inaccurate,
            is_old=is_old,
            location_finished=location_finished,
            location_type=location_type,
            vertical_accuracy=vertical_accuracy,
            timestamp=t_date,
            found_location_name=found_location_name,
        )
    except Exception as exc:
        logging.info('[iPhone last known location task] Error --> {exc}'.format(exc=exc))

        self.retry(
            countdown=backoff(self.request.retries),
            exc=exc
        )

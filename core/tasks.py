# -*- coding: utf-8 -*-

import logging

from celery import shared_task
from django.utils.timezone import now

from core.models import ExceptionStorage
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

    user_devices = [x for x in get_user_data if x]

    try:
        for user_device in user_devices:
            UserDevices.objects.get_or_create(
                device_name=user_device
            )

    except Exception as exc:
        logging.info('[Get user devices task] Error --> {exc}'.format(exc=exc))

        ExceptionStorage.objects.create(
            task_type=1,
            error_message=exc,
            timestamp=now()
        )

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
        iphone.iphone_name = device_name
        iphone.device_display_name = device_display_name
        iphone.battery_level = device_battery_level
        iphone.device_status = device_status
        iphone.save()

    except Exception as exc:
        logging.info('[iPhone status task] Error --> {exc}'.format(exc=exc))

        ExceptionStorage.objects.create(
            task_type=2,
            error_message=exc,
            timestamp=now()
        )

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

        ExceptionStorage.objects.create(
            task_type=3,
            error_message=exc,
            timestamp=now()
        )

        self.retry(
            countdown=backoff(self.request.retries),
            exc=exc
        )


@shared_task(
    name='get_user_contacts_task',
    queue='update_icloud_data',
    max_retries=10,
    bind=True,
)
def get_user_contacts_task(self):
    """
    Celery task to call iCloud API and retrieve all contacts data.
    """

    from core.models import iCloudContact
    from core.utils import get_user_contacts_data, get_user_contacts

    api = get_icloud_api_object()
    contacts_data = get_user_contacts(api)
    contacts = get_user_contacts_data(contacts_data)

    if contacts:
        try:
            for contact in contacts:
                iCloudContact.objects.get_or_create(
                    contact_id=contact[0],
                    first_name=contact[1],
                    middle_name=contact[2],
                    last_name=contact[3],
                    photo_url=contact[4],
                    etag=contact[5],
                    is_company=contact[6],
                    normalized=contact[7],
                    phone_number=contact[8],
                    phone_label=contact[9],
                    prefix=contact[10],
                    suffix=contact[11]
                )

        except Exception as exc:
            logging.info('[iPhone contacts task] Error --> {exc}'.format(exc=exc))

            ExceptionStorage.objects.create(
                task_type=4,
                error_message=exc,
                timestamp=now()
            )

            self.retry(
                countdown=backoff(self.request.retries),
                exc=exc
            )


@shared_task(
    name='get_user_calendar_events_task',
    queue='update_icloud_data',
    max_retries=10,
    bind=True,
)
def get_user_calendar_events_task(self):
    """
    Celery task to call iCloud API and retrieve all calendar events data.
    """

    from core.models import iCloudCalendar
    from core.utils import get_user_calendar_events, get_user_calendar_events_data

    api = get_icloud_api_object()
    calendar_data = get_user_calendar_events(api)
    calendars = get_user_calendar_events_data(calendar_data)

    if calendars:
        try:
            for calendar_item in calendars:
                iCloudCalendar.objects.get_or_create(
                    start_date=calendar_item[0],
                    end_date=calendar_item[1],
                    local_start_date=calendar_item[2],
                    local_end_date=calendar_item[3],
                    title=calendar_item[4],
                    tz=calendar_item[5],
                    is_all_day=calendar_item[6],
                    duration=calendar_item[7],
                    p_guid=calendar_item[8],
                )

        except Exception as exc:
            logging.info('[iPhone calendar task] Error --> {exc}'.format(exc=exc))

            ExceptionStorage.objects.create(
                task_type=5,
                error_message=exc,
                timestamp=now()
            )

            self.retry(
                countdown=backoff(self.request.retries),
                exc=exc
            )
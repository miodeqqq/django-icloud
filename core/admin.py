# -*- coding: utf-8 -*-

from django import forms
from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.db import models
from solo.admin import SingletonModelAdmin

from core.models import SendMessageToiPhone, GoogleMapsAPIKey, iCloudCalendar
from core.models import UserAuthentication, iPhoneStatus, iCloudContact
from core.models import iPhoneLastKnownLocation, UserDevices, ExceptionStorage


@admin.register(iCloudCalendar)
class iCloudCalendarAdmin(admin.ModelAdmin):
    """
    iCloud Calendar admin manager.
    """

    @classmethod
    def has_add_permission(self, request, obj=None):
        return False

    list_display = (
        'title',
        'start_date',
        'end_date',
        'local_start_date',
        'local_end_date',
        'tz',
        'is_all_day',
        'duration',
        'p_guid',
    )

    readonly_fields = (
        'title',
        'start_date',
        'end_date',
        'local_start_date',
        'local_end_date',
        'tz',
        'is_all_day',
        'duration',
        'p_guid',
    )

    list_filter = (
        'start_date',
        'end_date',
        'local_start_date',
        'local_end_date',
    )

    search_fields = (
        'title',
    )

    list_per_page = 20


@admin.register(ExceptionStorage)
class ExceptionStorageAdmin(admin.ModelAdmin):
    """
    Celery tasks/iCloud requests exceptions/errors admin manager.
    """

    @classmethod
    def has_add_permission(self, request, obj=None):
        return False

    list_display = (
        'task_type',
        'error_message',
        'timestamp',
    )

    readonly_fields = (
        'task_type',
        'error_message',
        'timestamp',
    )

    list_filter = (
        'task_type',
    )

    list_per_page = 20


class ShowContactsOnlyWithPhoto(SimpleListFilter):
    """
    Filter for iCloudContact model to filter only objects with condition "photo_url__isnull=False".
    """

    title = 'Only with photo'
    parameter_name = 'photo_url'

    def lookups(self, request, model_admin):
        return (
            ('0', 'No'),
            ('1', 'Yes'),
        )

    def queryset(self, request, queryset):
        if self.value() == '1':
            contact_ids = queryset.order_by(
                'pk'
            ).filter(
                photo_url__isnull=False
            ).values_list(
                'pk',
                flat=True
            )

            return queryset.filter(pk__in=contact_ids)

        return queryset


@admin.register(iCloudContact)
class iCloudContactAdmin(admin.ModelAdmin):
    """
    iCloud Contacts admin manager.
    """

    list_display = (
        'pk',
        'first_name',
        'last_name',
        'contact_image',
        'phone_number',
        'phone_label'
    )

    readonly_fields = (
        'contact_id',
        'first_name',
        'middle_name',
        'last_name',
        'photo_url',
        'etag',
        'is_company',
        'normalized',
        'phone_number',
        'phone_label',
        'prefix',
        'suffix',
    )

    search_fields = (
        'first_name',
        'last_name',
        'phone_number'
    )

    list_filter = (
        ShowContactsOnlyWithPhoto,
    )

    list_per_page = 20

    def contact_image(self, obj):
        """
        Returns contact image for if found.
        """

        return '<img class="img-responsive" src="{img_url}" width="100" height="100"/>'.format(
            img_url=obj.photo_url
        ) if obj.photo_url else '<span style="color:red">Not found...</span>'

    contact_image.allow_tags = True
    contact_image.short_description = u'Photo'


@admin.register(GoogleMapsAPIKey)
class GoogleMapsAPIKeyAdmin(SingletonModelAdmin):
    """
    Google Maps API key admin manager.
    """

    formfield_overrides = {
        models.CharField: {
            'widget': forms.Textarea(attrs={
                'rows': 1,
                'cols': 40,
                'style': 'width: 65%;',
            })
        }
    }


@admin.register(UserAuthentication)
class UserAuthenticationAdmin(SingletonModelAdmin):
    """
    iCloud user authentication manager.
    """

    fieldsets = [
        (u'E-MAIL', {
            'fields': [
                'email',
            ]
        }),
        (u'PASSWORD', {
            'fields': [
                'password',
            ]
        }),
    ]


@admin.register(iPhoneStatus)
class iPhoneStatusAdmin(SingletonModelAdmin):
    """
    iPhone status admin manager.
    """

    readonly_fields = (
        'iphone_name',
        'device_display_name',
        'get_battery_percentage',
        'device_status',
    )

    exclude = (
        'battery_level',
    )

    def get_battery_percentage(self, obj):
        """
        Returns iPhone's battery percentage status.
        """

        if obj.battery_level:
            return '{:0.2f} %'.format(obj.battery_level)
        else:
            return '{0:.2f} %'.format(float(0))

    get_battery_percentage.allow_tags = True
    get_battery_percentage.short_description = 'Battery percentage'


@admin.register(iPhoneLastKnownLocation)
class iPhoneLastKnownLocationAdmin(admin.ModelAdmin):
    """
    iPhone last known locations admin manager.
    """

    @classmethod
    def has_add_permission(self, request, obj=None):
        return False

    list_display = (
        'found_location_name',
        'position_type',
        'latitude',
        'longitude',
        'timestamp',
        'get_map_location'
    )

    list_filter = (
        'found_location_name',
        'position_type'
    )

    readonly_fields = (
        'found_location_name',
        'position_type',
        'altitude',
        'latitude',
        'longitude',
        'floor_level',
        'horizontal_accuracy',
        'is_inaccurate',
        'is_old',
        'location_finished',
        'location_type',
        'vertical_accuracy',
        'timestamp',
        'get_map_location'
    )

    search_fields = (
        'found_location_name',
    )

    list_per_page = 10

    def get_map_location(self, obj):
        """
        Redirects to Google Map with last known location.
        """

        if obj.latitude and obj.longitude:
            location_name = obj.found_location_name

            return '<a href="/map/{obj_pk}/" target="_blank">Show location on map</a>'.format(
                obj_pk=obj.pk,
                location_name=location_name
            )

        return '<span style="color:red">Not yet...</span>'

    get_map_location.allow_tags = True
    get_map_location.short_description = 'Map'


@admin.register(UserDevices)
class UserDevicesAdmin(admin.ModelAdmin):
    """
    iCloud devices admin manager.
    """

    @classmethod
    def has_add_permission(self, request, obj=None):
        return False

    list_display = (
        'device_name',
    )

    readonly_fields = (
        'device_name',
    )

    list_per_page = 30


@admin.register(SendMessageToiPhone)
class SendMessageToiPhoneAdmin(admin.ModelAdmin):
    """
    iCloud lost device(iPhone) admin manager.
    """

    list_display = (
        'phone_number',
        'message',
        'status',
        'timestamp',
    )

    readonly_fields = (
        'status',
    )

    list_filter = (
        'status',
    )

    list_per_page = 30


# we're not using these modules
# admin.site.unregister(WorkerState)
# admin.site.unregister(TaskState)
# admin.site.unregister(IntervalSchedule)

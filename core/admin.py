# -*- coding: utf-8 -*-
from django import forms
from django.contrib import admin
from django.db import models
from djcelery.models import (TaskState, WorkerState, IntervalSchedule)
from solo.admin import SingletonModelAdmin

from core.models import SendMessageToiPhone, GoogleMapsAPIKey
from core.models import UserAuthentication, iPhoneStatus
from core.models import iPhoneLastKnownLocation, UserDevices


@admin.register(GoogleMapsAPIKey)
class GoogleMapsAPIKeyAdmin(SingletonModelAdmin):
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
    readonly_fields = (
        'iphone_name',
        'device_display_name',
        'get_battery_percentage',
        'device_status',
    )

    exclude = (
        'battery_level',
    )

    list_per_page = 30

    def get_battery_percentage(self, obj):
        """
        Returns iPhone's battery percentage status.
        """

        if obj.battery_level:
            return '{0:.2f} %'.format(obj.battery_level)
        else:
            return '{0:.2f} %'.format(float(0))

    get_battery_percentage.allow_tags = True
    get_battery_percentage.short_description = 'Battery percentage'


@admin.register(iPhoneLastKnownLocation)
class iPhoneLastKnownLocationAdmin(admin.ModelAdmin):
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

    list_per_page = 30

    def get_map_location(self, obj):
        """
        Redirects to Google Map with last known location.
        """

        if obj.latitude and obj.longitude:
            location_name = obj.found_location_name

            return '<a href="/map/{obj_pk}/" target="_blank">{location_name}</a>'.format(
                obj_pk=obj.pk,
                location_name=location_name
            )

        return '<span style="color:red">Not yet...</span>'

    get_map_location.allow_tags = True
    get_map_location.short_description = 'Map'


@admin.register(UserDevices)
class UserDevicesAdmin(admin.ModelAdmin):
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
admin.site.unregister(WorkerState)
admin.site.unregister(TaskState)
admin.site.unregister(IntervalSchedule)

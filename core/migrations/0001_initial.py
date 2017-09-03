# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ExceptionStorage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('task_type', models.PositiveSmallIntegerField(verbose_name='Task type', db_index=True, choices=[(1, 'get_user_devices_task'), (2, 'get_user_iphone_status_task'), (3, 'get_user_iphone_location_task'), (4, 'get_user_contacts_task'), (5, 'get_user_calendar_events_task'), (6, 'send_message_to_iphone')])),
                ('error_message', models.TextField(verbose_name='Error message')),
                ('timestamp', models.DateTimeField(verbose_name='Timestamp', auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Error',
                'verbose_name_plural': 'Errors',
            },
        ),
        migrations.CreateModel(
            name='GoogleMapsAPIKey',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('api_key', models.CharField(verbose_name='API key', max_length=255, db_index=True)),
            ],
            options={
                'verbose_name': 'Google Maps API key',
            },
        ),
        migrations.CreateModel(
            name='iCloudCalendar',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('start_date', models.DateTimeField(verbose_name='Start date', db_index=True, editable=False)),
                ('end_date', models.DateTimeField(verbose_name='End date', db_index=True, editable=False)),
                ('local_start_date', models.DateTimeField(verbose_name='Local start date', db_index=True, editable=False)),
                ('local_end_date', models.DateTimeField(verbose_name='Local end date', db_index=True, editable=False)),
                ('title', models.CharField(verbose_name='Title', max_length=255, blank=True, null=True, db_index=True)),
                ('tz', models.CharField(verbose_name='TZ', max_length=255, blank=True, null=True, db_index=True)),
                ('is_all_day', models.BooleanField(verbose_name='Is all day ?', db_index=True, default=False)),
                ('duration', models.PositiveSmallIntegerField(verbose_name='Duration', blank=True, null=True, db_index=True)),
                ('p_guid', models.CharField(verbose_name='P Guid', max_length=255, blank=True, null=True, db_index=True)),
            ],
            options={
                'verbose_name': 'iCloud calendar event',
                'verbose_name_plural': 'iCloud calendar events',
            },
        ),
        migrations.CreateModel(
            name='iCloudContact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('contact_id', models.CharField(verbose_name='Contact ID', max_length=255, unique=True, db_index=True)),
                ('first_name', models.CharField(verbose_name='First name', max_length=255, blank=True, null=True, db_index=True)),
                ('middle_name', models.CharField(verbose_name='Middle name', max_length=255, blank=True, null=True, db_index=True)),
                ('last_name', models.CharField(verbose_name='Last name', max_length=255, blank=True, null=True, db_index=True)),
                ('photo_url', models.URLField(verbose_name='Photo URL', max_length=500, blank=True, null=True, db_index=True)),
                ('etag', models.CharField(verbose_name='Etag', max_length=255, blank=True, null=True, db_index=True)),
                ('is_company', models.BooleanField(verbose_name='Is company?', db_index=True, default=False)),
                ('normalized', models.CharField(verbose_name='Normalized', max_length=255, blank=True, null=True, db_index=True)),
                ('phone_number', models.CharField(verbose_name='Phone number(s)', max_length=255, blank=True, null=True, db_index=True)),
                ('phone_label', models.CharField(verbose_name='Phone label', max_length=255, blank=True, null=True, db_index=True)),
                ('prefix', models.CharField(verbose_name='Prefix', max_length=255, blank=True, null=True, db_index=True)),
                ('suffix', models.CharField(verbose_name='Suffix', max_length=255, blank=True, null=True, db_index=True)),
            ],
            options={
                'verbose_name': 'iCloud contact',
                'verbose_name_plural': 'iCloud contacts',
            },
        ),
        migrations.CreateModel(
            name='iPhoneLastKnownLocation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('position_type', models.CharField(verbose_name='Position type', max_length=255, blank=True, db_index=True)),
                ('altitude', models.FloatField(verbose_name='Altitude', blank=True, null=True, db_index=True)),
                ('latitude', models.FloatField(verbose_name='Latitude', blank=True, null=True, db_index=True)),
                ('longitude', models.FloatField(verbose_name='Longitude', blank=True, null=True, db_index=True)),
                ('floor_level', models.PositiveSmallIntegerField(verbose_name='Floor level', blank=True, db_index=True, default=0)),
                ('horizontal_accuracy', models.FloatField(verbose_name='Horizontal accuracy', blank=True, null=True, db_index=True)),
                ('is_inaccurate', models.BooleanField(verbose_name='Is inaccurate ?', default=False)),
                ('is_old', models.BooleanField(verbose_name='Is old ?', db_index=True, default=False)),
                ('location_finished', models.BooleanField(verbose_name='Location finished', db_index=True, default=False)),
                ('location_type', models.CharField(verbose_name='Location type', max_length=255, blank=True, db_index=True)),
                ('vertical_accuracy', models.FloatField(verbose_name='Vertical accuracy', blank=True, null=True, db_index=True)),
                ('timestamp', models.DateTimeField(verbose_name='Timestamp', db_index=True, editable=False)),
                ('found_location_name', models.TextField(verbose_name='Location', blank=True, db_index=True)),
            ],
            options={
                'verbose_name': "iPhone's last known location",
                'verbose_name_plural': "iPhone's last known locations",
            },
        ),
        migrations.CreateModel(
            name='iPhoneStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('iphone_name', models.CharField(verbose_name='Device name', max_length=255, blank=True, db_index=True)),
                ('device_display_name', models.CharField(verbose_name='Device display name', max_length=255, blank=True, db_index=True)),
                ('battery_level', models.FloatField(verbose_name='Battery level', blank=True, null=True, db_index=True)),
                ('device_status', models.CharField(verbose_name='Device status', max_length=255, blank=True, db_index=True)),
            ],
            options={
                'verbose_name': 'iPhone status',
            },
        ),
        migrations.CreateModel(
            name='SendMessageToiPhone',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('phone_number', models.CharField(verbose_name='Phone number', max_length=255)),
                ('message', models.CharField(verbose_name='Message', max_length=255)),
                ('status', models.BooleanField(verbose_name='Sending status', db_index=True, default=False)),
                ('timestamp', models.DateTimeField(verbose_name='Date', db_index=True, auto_now_add=True)),
            ],
            options={
                'verbose_name': 'iPhone lost mode message',
                'verbose_name_plural': 'iPhone lost mode messages',
            },
        ),
        migrations.CreateModel(
            name='UserAuthentication',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('email', models.EmailField(verbose_name='Username', max_length=255, db_index=True)),
                ('password', models.CharField(verbose_name='Password', max_length=255, db_index=True)),
            ],
            options={
                'verbose_name': "iCloud User's authentication",
            },
        ),
        migrations.CreateModel(
            name='UserDevices',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('device_name', models.CharField(verbose_name='Device', max_length=255, blank=True)),
            ],
            options={
                'verbose_name': 'iCloud device',
                'verbose_name_plural': "iCloud's devices",
            },
        ),
    ]

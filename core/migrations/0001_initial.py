# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
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
                'verbose_name': 'iPhone device status',
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
                'verbose_name': "User's authentication",
            },
        ),
        migrations.CreateModel(
            name='UserDevices',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('device_name', models.CharField(verbose_name='Device', max_length=255, blank=True)),
            ],
            options={
                'verbose_name': 'User device',
                'verbose_name_plural': "User's devices",
            },
        ),
    ]

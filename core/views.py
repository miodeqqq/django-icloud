# -*- coding: utf-8 -*-

from statistics import median

from django.http import Http404
from django.shortcuts import render, get_object_or_404

from core.models import iPhoneLastKnownLocation, GoogleMapsAPIKey


def show_map(request, object_pk):
    template = 'map.html'

    try:
        map_object = get_object_or_404(iPhoneLastKnownLocation, id=object_pk)
    except iPhoneLastKnownLocation.DoesNotExist:
        raise Http404

    try:
        api_key = GoogleMapsAPIKey.get_solo().api_key
    except GoogleMapsAPIKey.DoesNotExist:
        raise Http404

    context = {
        'latitude': map_object.latitude,
        'longitude': map_object.longitude,
        'api_key': api_key,
        'location': map_object.found_location_name,
        'timestamp': map_object.timestamp
    }

    return render(request, template, context)


def show_draw_map(request):
    """
    Returns a draw map of locations.
    """

    template = 'show_route.html'

    try:
        coordinates = iPhoneLastKnownLocation.objects.values_list('latitude', 'longitude')

        start_coordinate_latitude = iPhoneLastKnownLocation.objects.first().latitude
        end_coordinate_latitude = iPhoneLastKnownLocation.objects.last().latitude
        avg_start_latitude = median([start_coordinate_latitude, end_coordinate_latitude])

    except iPhoneLastKnownLocation.DoesNotExist:
        raise Http404

    try:
        api_key = GoogleMapsAPIKey.get_solo().api_key
    except GoogleMapsAPIKey.DoesNotExist:
        raise Http404

    context = {
        'start_coordinate': avg_start_latitude,
        'coordinates': coordinates,
        'api_key': api_key,
    }

    return render(request, template, context)

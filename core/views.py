# -*- coding: utf-8 -*-

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

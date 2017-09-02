# -*- coding: utf-8 -*-

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^map/(?P<object_pk>[\w\-_]+)/$', views.show_map, name='show_map')
]

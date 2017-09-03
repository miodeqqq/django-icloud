# -*- coding: utf-8 -*-

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^map/(?P<object_pk>[\w\-_]+)/$', views.show_map, name='show_map'),
    url(r'^show_route/$', views.show_draw_map, name='show_draw_map')
]

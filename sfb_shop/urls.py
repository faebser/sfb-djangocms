# -*- coding: utf-8 -*-
__author__ = 'faebser'
from django.conf.urls import patterns, url

from sfb_shop import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index')
)
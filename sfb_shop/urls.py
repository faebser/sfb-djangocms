# -*- coding: utf-8 -*-
__author__ = 'faebser'
from django.conf.urls import patterns, url

from sfb_shop import views

urlpatterns = patterns('',
    url(r'^test/$', views.index, name='index'),
    url(r'^form/$', views.get_form, name='form'),
    url(r'^addToCart/$',views.addToCart, name=u'cart'),
    url(r'^checkout/$', views.checkout, name='checkout')
)
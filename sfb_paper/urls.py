__author__ = 'faebser'

from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',
    url(r'^issue/(?P<issue_pk>[0-9]+)/$', views.get_issue_from_id, name='get_issue_form_id'),
    url(r'^tags/(?P<tags>[0-9A-Za-z-_.//]+)/$', views.get_articles_from_tags, name='get_articles_from_tags'),
)
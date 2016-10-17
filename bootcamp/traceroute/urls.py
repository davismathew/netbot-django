# coding: utf-8

from django.conf.urls import patterns, include, url
from django.views.decorators.csrf import csrf_exempt

from bootcamp.traceroute import views

urlpatterns = [
    url(r'^$', views.traceroute, name='traceroute'),
    url(r'^mtn/$', views.mtntraceroute, name='mtntraceroute'),
    url(r'^gettrace/$', views.gettraceroute, name='gettrace'),
    url(r'^runtraceroute/$', csrf_exempt(views.runtraceroute), name='runtraceroute'),
    # url(r'^preview/$', views.preview, name='preview'),
    # url(r'^drafts/$', views.drafts, name='drafts'),
    # url(r'^comment/$', views.comment, name='comment'),
    # url(r'^tag/(?P<tag_name>.+)/$', views.tag, name='tag'),
    # url(r'^edit/(?P<id>\d+)/$', views.edit, name='edit_article'),
    # url(r'^(?P<slug>[-\w]+)/$', views.article, name='article'),
]
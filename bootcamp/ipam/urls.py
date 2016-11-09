# coding: utf-8

from django.conf.urls import patterns, include, url
from django.views.decorators.csrf import csrf_exempt

from bootcamp.ipam import views

urlpatterns = [
    url(r'^$', views.dispcheckipam, name='checkipam'),
    url(r'^fetchipamcheck/$', views.fetchipamcheck, name='fetchipamcheck'),
    url(r'^runipamcheck/$', csrf_exempt(views.runipamcheck), name='runipamcheck'),
    # url(r'^preview/$', views.preview, name='preview'),
    # url(r'^drafts/$', views.drafts, name='drafts'),
    # url(r'^comment/$', views.comment, name='comment'),
    # url(r'^tag/(?P<tag_name>.+)/$', views.tag, name='tag'),
    # url(r'^edit/(?P<id>\d+)/$', views.edit, name='edit_article'),
    # url(r'^(?P<slug>[-\w]+)/$', views.article, name='article'),
]
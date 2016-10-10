# coding: utf-8

from django.conf.urls import patterns, include, url
from django.views.decorators.csrf import csrf_exempt
from bootcamp.results import views

urlpatterns = [
    url(r'^$', views.results, name='results'),
    url(r'^createresult/$', views.createresult, name='createresult'),
    url(r'^testpost/$', csrf_exempt(views.testpost), name='testpost'),
    url(r'^cmapp/$', csrf_exempt(views.cmapp), name='cmapp'),
    url(r'^resultdetails/(?P<id>\d+)/$', csrf_exempt(views.resultdetails), name='resultdetails'),
    # url(r'^preview/$', views.preview, name='preview'),
    # url(r'^drafts/$', views.drafts, name='drafts'),
    # url(r'^comment/$', views.comment, name='comment'),
    # url(r'^tag/(?P<tag_name>.+)/$', views.tag, name='tag'),
    # url(r'^edit/(?P<id>\d+)/$', views.edit, name='edit_article'),
    # url(r'^(?P<slug>[-\w]+)/$', views.article, name='article'),
]
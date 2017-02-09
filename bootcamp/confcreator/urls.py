# coding: utf-8

from django.conf.urls import patterns, include, url
from django.views.decorators.csrf import csrf_exempt

from bootcamp.confcreator import views

urlpatterns = [
    url(r'^$', views.listcreator, name='listcreator'),
    url(r'^createconfcreator/$', csrf_exempt(views.createconfcreator), name='createconfcreator'),
    url(r'^executecommand/(?P<id>\d+)/$', csrf_exempt(views.executecommand), name='executecommand'),
    url(r'^runcommand/$', csrf_exempt(views.runcommand), name='runcommand'),
    url(r'^runcommandoutapi/$', csrf_exempt(views.runcommandoutapi), name='runcommandoutapi'),
    # url(r'^createconf/$', views.createconftemplate, name='createconf'),
    # url(r'^downloadtemplateout/(?P<id>\d+)/$', csrf_exempt(views.downloadtemplateout), name='downloadtemplateout'),
    # url(r'^fetchipamcheck/$', views.fetchipamcheck, name='fetchipamcheck'),
    # url(r'^runipamcheck/$', csrf_exempt(views.runipamcheck), name='runipamcheck'),
    # url(r'^preview/$', views.preview, name='preview'),
    # url(r'^drafts/$', views.drafts, name='drafts'),
    # url(r'^comment/$', views.comment, name='comment'),
    # url(r'^tag/(?P<tag_name>.+)/$', views.tag, name='tag'),
    # url(r'^edit/(?P<id>\d+)/$', views.edit, name='edit_article'),
    # url(r'^(?P<slug>[-\w]+)/$', views.article, name='article'),
]
# coding: utf-8

from django.conf.urls import patterns, include, url

from bootcamp.tasks import views

urlpatterns = [
    url(r'^$', views.tasks, name='tasks'),
    url(r'^createtask/$', views.createtask, name='createtask'),
    url(r'^edit/(?P<id>\d+)/$', views.edit, name='edit_task'),
    url(r'^runtask/(?P<id>\d+)/$', views.runtask, name='runtask'),
    # url(r'^preview/$', views.preview, name='preview'),
    # url(r'^drafts/$', views.drafts, name='drafts'),
    # url(r'^comment/$', views.comment, name='comment'),
    # url(r'^tag/(?P<tag_name>.+)/$', views.tag, name='tag'),
    # url(r'^edit/(?P<id>\d+)/$', views.edit, name='edit_article'),
    # url(r'^(?P<slug>[-\w]+)/$', views.article, name='article'),
]
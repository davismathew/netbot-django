# coding: utf-8

from django.conf.urls import patterns, include, url

from bootcamp.cmapp import views

urlpatterns = [
    url(r'^$', views.emccm, name='cmapp'),
    url(r'^emccm/$', views.emccm, name='emccm'),
    url(r'^mtncm/$', views.mtncm, name='mtncm'),
    # url(r'^inventorydetails/(?P<id>\d+)/$', views.inventorydetails, name='inventorydetails'),
    # url(r'^preview/$', views.preview, name='preview'),
    # url(r'^drafts/$', views.drafts, name='drafts'),
    # url(r'^comment/$', views.comment, name='comment'),
    # url(r'^tag/(?P<tag_name>.+)/$', views.tag, name='tag'),
    # url(r'^edit/(?P<id>\d+)/$', views.edit, name='edit_article'),
    # url(r'^(?P<slug>[-\w]+)/$', views.article, name='article'),
]
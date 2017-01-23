# coding: utf-8

from django.conf.urls import patterns, include, url
from django.views.decorators.csrf import csrf_exempt
from bootcamp.cmapp import views

urlpatterns = [
    url(r'^$', views.emccm, name='cmapp'),
    url(r'^emccm/$', views.emccm, name='emccm'),
    url(r'^mtncm/$', views.mtncm, name='mtncm'),
    url(r'^testmodal/$', views.testmodal, name='testmodal'),
    url(r'^newmodal/$', views.newmodal, name='newmodal'),
    url(r'^testapi/$', views.testapi, name='testapi'),
    url(r'^coreCircuitStates/(?P<id>\d+)/$', csrf_exempt(views.coreCircuitStates), name='coreCircuitStates'),
    url(r'^coreCircuitDetails/(?P<id>\d+)/$', csrf_exempt(views.coreCircuitDetails), name='coreCircuitDetails'),
    url(r'^orionNodeStates/(?P<id>\d+)/$', csrf_exempt(views.orionNodeStates), name='orionNodeStates'),
    url(r'^rowPingTest/(?P<id>\d+)/$', csrf_exempt(views.rowPingTest), name='rowPingTest'),
    url(r'^allRowPingTest/$', csrf_exempt(views.allRowPingTest), name='allRowPingTest'),
    url(r'^delCCSRecord/$', csrf_exempt(views.delCCSRecord), name='delCCSRecord'),
    url(r'^delONSRecord/$', csrf_exempt(views.delONSRecord), name='delONSRecord'),
    # url(r'^inventorydetails/(?P<id>\d+)/$', views.inventorydetails, name='inventorydetails'),
    # url(r'^preview/$', views.preview, name='preview'),
    # url(r'^drafts/$', views.drafts, name='drafts'),
    # url(r'^comment/$', views.comment, name='comment'),
    # url(r'^tag/(?P<tag_name>.+)/$', views.tag, name='tag'),
    # url(r'^edit/(?P<id>\d+)/$', views.edit, name='edit_article'),
    # url(r'^(?P<slug>[-\w]+)/$', views.article, name='article'),
]
from .views import DefaultCustomDashboard, PublicDashboard

from django.conf.urls import *


# place app url patterns here

urlpatterns = patterns('',


                       #display public custom dashboard
                       url(r'^public/(?P<id>\w+)/$', 'customdashboard.views.PublicDashboard', name='public_dashboard'),
                       url(r'^public/(?P<id>\w+)/([0-9]+)/$', 'customdashboard.views.PublicDashboard', name='public_dashboard'),

                       #display default custom dashboard
                       url(r'^(?P<id>\w+)/$', 'customdashboard.views.DefaultCustomDashboard', name='default_custom_dashboard'),
                       url(r'^(?P<id>\w+)/([0-9]+)/$', 'customdashboard.views.DefaultCustomDashboard', name='default_custom_dashboard'),


                       #project status
                       url(r'^(?P<id>[0-9]+)/(?P<status>[\w ]+)/$', 'customdashboard.views.DefaultCustomDashboard', name='project_status'),

                       #gallery
                       url(r'^public/(?P<id>\w+)/gallery/([0-9]+)/$', 'customdashboard.views.Gallery', name='gallery'),
                       url(r'^public/(?P<id>\w+)/([0-9]+)/gallery/([0-9]+)/$', 'customdashboard.views.Gallery', name='gallery'),
                       )



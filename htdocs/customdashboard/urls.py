from .views import CustomDashboard

from django.conf.urls import *

# place app url patterns here

urlpatterns = patterns('',

                       #display default custom dashboard
                       url(r'^customdashboard/(?P<id>\w+)/(?P<sector>\w+)/$', 'customdashboard.views.DefaultCustomDashboard', name='default_custom_dashboard'),

                       )

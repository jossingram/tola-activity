from .views import DefaultCustomDashboard

from django.conf.urls import *

# place app url patterns here

urlpatterns = patterns('',
                       #display default custom dashboard
                        url(r'^$', 'customdashboard.views.DefaultCustomDashboard', name='default_custom_dashboard'),
                       )

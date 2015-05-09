from django.conf.urls import patterns, include, url

from .views import QuantitativeOutputsList, QuantitativeOutputsCreate, QuantitativeOutputsUpdate, QuantitativeOutputsDelete


urlpatterns = patterns('',

    ###INDICATOR PLANING TOOL
    #Home
    url(r'^home/(?P<id>\w+)/$', 'indicators.views.home', name='home'),
    
    #Dashboard
    url(r'^dashboard', 'indicators.views.dashboard', name='dashboard'),

    #View Program Indicators
    url(r'^programIndicator/(?P<id>\w+)/$', 'indicators.views.programIndicator', name='programIndicator'),
    
    #Edit Indicators to Program
    url(r'^editIndicator/(?P<id>\w+)/$', 'indicators.views.editIndicator', name='editIndicator'),
    
    #Add Indicators to Program
    url(r'^indicator', 'indicators.views.indicator', name='indicator'),

    #Indicator Report
    url(r'^report', 'indicators.views.indicatorReport', name='indicatorReport'),

    #Indicator Form
    url(r'^form/(?P<pk>\w+)/$', QuantitativeOutputsList.as_view(), name='quantitative_list'),
    url(r'^quantitative_add/(?P<id>\w+)/$', QuantitativeOutputsCreate.as_view(), name='quantitative_add'),
    url(r'^quantitative_update/(?P<pk>\w+)/$', QuantitativeOutputsUpdate.as_view(), name='quantitative_update'),
    url(r'^quantitative_delete/(?P<pk>\w+)/$', QuantitativeOutputsDelete.as_view(), name='quantitative_delete'),

    #Indicator Data Report
    url(r'^data/(?P<id>\w+)/$', 'indicators.views.indicatorDataReport', name='indicatorDataReport'),
    
)
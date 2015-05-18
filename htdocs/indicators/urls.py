from django.conf.urls import patterns, include, url

from .views import QuantitativeOutputsList, QuantitativeOutputsCreate, QuantitativeOutputsUpdate, QuantitativeOutputsDelete,\
    CollectedDataList, CollectedDataCreate, CollectedDataUpdate, CollectedDataDelete, IndicatorCreate, IndicatorDelete, IndicatorUpdate,\
    IndicatorList


urlpatterns = patterns('',

    ###INDICATOR PLANING TOOL
    #Home
    url(r'^home/(?P<pk>\w+)/$', IndicatorList.as_view(), name='indicator_list'),

    #Indicator Report
    url(r'^report', 'indicators.views.indicatorReport', name='indicatorReport'),
    
    #Indicator Form
    url(r'^indicator_list/(?P<pk>\w+)/$', IndicatorList.as_view(), name='indicator_list'),
    url(r'^indicator_add/(?P<id>\w+)/$', IndicatorCreate.as_view(), name='indicator_add'),
    url(r'^indicator_update/(?P<pk>\w+)/$', IndicatorUpdate.as_view(), name='indicator_update'),
    url(r'^indicator_delete/(?P<pk>\w+)/$', IndicatorDelete.as_view(), name='indicator_delete'),

    #Quantitative OUtputs Form
    url(r'^form/(?P<pk>\w+)/$', QuantitativeOutputsList.as_view(), name='quantitative_list'),
    url(r'^quantitative_add/(?P<id>\w+)/$', QuantitativeOutputsCreate.as_view(), name='quantitative_add'),
    url(r'^quantitative_update/(?P<pk>\w+)/$', QuantitativeOutputsUpdate.as_view(), name='quantitative_update'),
    url(r'^quantitative_delete/(?P<pk>\w+)/$', QuantitativeOutputsDelete.as_view(), name='quantitative_delete'),

    #Collected Data Form
    url(r'^collecteddata/(?P<pk>\w+)/$', CollectedDataList.as_view(), name='collecteddata_list'),
    url(r'^collecteddata/(?P<pk>\w+)/(?P<program>\w+)/$', CollectedDataList.as_view(), name='collecteddata_list'),
    url(r'^collecteddata/(?P<pk>\w+)/(?P<program>\w+)/(?P<agreement>\w+)/$', CollectedDataList.as_view(), name='collecteddata_list'),

    url(r'^collecteddata_add/(?P<id>\w+)/$', CollectedDataCreate.as_view(), name='collecteddata_add'),
    url(r'^collecteddata_update/(?P<pk>\w+)/$', CollectedDataUpdate.as_view(), name='collecteddata_update'),
    url(r'^collecteddata_delete/(?P<pk>\w+)/$', CollectedDataDelete.as_view(), name='collecteddata_delete'),

    #Indicator Data Report
    url(r'^data/(?P<id>\w+)/$', 'indicators.views.indicatorDataReport', name='indicatorDataReport'),
    url(r'^data/(?P<id>\w+)/map/$', 'indicators.views.indicatorDataReport', name='indicatorDataReport'),
    url(r'^data/(?P<id>\w+)/graph/$', 'indicators.views.indicatorDataReport', name='indicatorDataReport'),
    url(r'^data/(?P<id>\w+)/(?P<program>\w+)/$', 'indicators.views.indicatorDataReport', name='indicatorDataReport'),
    url(r'^data/(?P<id>\w+)/(?P<program>\w+)/(?P<agreement>\w+)/$', 'indicators.views.indicatorDataReport', name='indicatorDataReport'),

    
)
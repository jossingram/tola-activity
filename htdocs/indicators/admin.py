from django.contrib import admin
from indicators.models import IndicatorType, Indicator, ReportingFrequency, DisaggregationType

admin.site.register(IndicatorType)
admin.site.register(Indicator)
admin.site.register(ReportingFrequency)
admin.site.register(DisaggregationType)

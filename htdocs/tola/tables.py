import django_tables2 as tables
from indicators.models import Indicator, CollectedData
from activitydb.models import QuantitativeOutputs
from django_tables2.utils import A

class IndicatorDataTable(tables.Table):

    agreement = tables.LinkColumn('projectagreement_update', args=[A('agreement_id')])

    class Meta:
        model = QuantitativeOutputs
        attrs = {"class": "paleblue"}
        fields = ('targeted', 'achieved', 'indicator', 'agreement', 'complete')
        sequence = ('targeted', 'achieved', 'indicator', 'agreement', 'complete')


class CollectedDataTable(tables.Table):

    agreement = tables.LinkColumn('projectagreement_update', args=[A('agreement_id')])

    class Meta:
        model = CollectedData
        attrs = {"class": "paleblue"}
        fields = ('targeted', 'achieved', 'description', 'logframe_indicator', 'sector', 'community', 'agreement', 'complete')
        sequence = ('targeted', 'achieved', 'description', 'logframe_indicator', 'sector', 'community', 'agreement', 'complete')
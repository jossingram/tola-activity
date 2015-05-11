import django_tables2 as tables
from models import Indicator, CollectedData
from activitydb.models import QuantitativeOutputs
from django_tables2.utils import A

TEMPLATE = '''
<div class="btn-group btn-group-xs">
   <a type="button" class="btn btn-warning" href="/indicators/indicator_update/{{ record.id }}">Edit</a>
   <a type="button" class="btn btn-default" href="/indicators/data/{{ record.id }}">View</a>
</div>
'''


class IndicatorTable(tables.Table):
    edit = tables.TemplateColumn(TEMPLATE)

    class Meta:
        model = Indicator
        attrs = {"class": "paleblue"}
        fields = ('indicator_type', 'name', 'number', 'source', 'definition', 'disaggregation', 'baseline', 'lop_target', 'means_of_verification', 'data_collection_method', 'responsible_person',
                    'method_of_analysis', 'information_use', 'reporting_frequency', 'comments', 'program', 'sector', 'approved_by', 'approval_submitted_by', 'create_date', 'edit_date')
        sequence = ('indicator_type', 'name', 'number', 'source', 'definition', 'disaggregation', 'baseline', 'lop_target', 'means_of_verification', 'data_collection_method', 'responsible_person',
                    'method_of_analysis', 'information_use', 'reporting_frequency', 'comments', 'program', 'sector', 'approved_by', 'approval_submitted_by', 'create_date', 'edit_date')


class IndicatorDataTable(tables.Table):

    agreement = tables.LinkColumn('projectagreement_update', args=[A('agreement_id')])

    class Meta:
        model = QuantitativeOutputs
        attrs = {"class": "paleblue"}
        fields = ('targeted', 'achieved', 'description', 'logframe_indicator', 'non_logframe_indicator', 'agreement', 'complete')
        sequence = ('targeted', 'achieved', 'description', 'logframe_indicator', 'non_logframe_indicator', 'agreement', 'complete')


class CollectedDataTable(tables.Table):

    agreement = tables.LinkColumn('projectagreement_update', args=[A('agreement_id')])

    class Meta:
        model = CollectedData
        attrs = {"class": "paleblue"}
        fields = ('targeted', 'achieved', 'description', 'logframe_indicator', 'non_logframe_indicator', 'sector', 'community', 'agreement', 'complete')
        sequence = ('targeted', 'achieved', 'description', 'logframe_indicator', 'non_logframe_indicator', 'sector', 'community', 'agreement', 'complete')
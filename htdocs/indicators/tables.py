import django_tables2 as tables
from models import Indicator

TEMPLATE = '''
<div class="btn-group btn-group-xs">
   <a type="button" class="btn btn-warning" href="/indicator/indicator_update/{{ record.id }}">Edit</a>
   <a type="button" class="btn btn-default" href="/indicator/indicator_detail/{{ record.id }}">View</a>
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

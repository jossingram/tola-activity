from django.forms import ModelForm
from indicators.models import Indicator, CollectedData
from activitydb.models import Program, QuantitativeOutputs
from crispy_forms.helper import FormHelper
from crispy_forms.layout import *
from crispy_forms.bootstrap import *
from crispy_forms.layout import Layout, Submit, Reset, Field

import floppyforms.__future__ as forms
from tola.util import getCountry


class IndicatorForm(forms.ModelForm):

    class Meta:
        model = Indicator
        exclude = ['create_date','edit_date']

    program = forms.ModelMultipleChoiceField(queryset=Program.objects.filter(funding_status="Funded"))

    def __init__(self, *args, **kwargs):
        #get the user object to check permissions with
        self.request = kwargs.pop('request')
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-6'
        self.helper.form_error_title = 'Form Errors'
        self.helper.error_text_inline = True
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.layout = Layout(

            HTML("""<br/>"""),
            TabHolder(
                Tab('Performance',
                     Fieldset('Performance',
                        'name', 'type', 'objectives', 'number', 'source', 'definition', 'disaggregation','owner','program','sector','indicator_type'
                        ),
                ),
                Tab('Targets',
                    Fieldset('Targets',
                             'baseline','lop_target',
                             ),
                ),
                Tab('Data Acquisition',
                    Fieldset('Data Acquisition',
                        'means_of_verification','data_collection_method','responsible_person',
                        ),
                ),
                Tab('Analyses and Reporting',
                    Fieldset('Analyses and Reporting',
                        'method_of_analysis','information_use', 'reporting_frequency','comments'
                    ),
                ),
                Tab('Approval',
                    Fieldset('Approval',
                        'approval', 'filled_by', 'approved_by',
                    ),
                ),
            ),

            HTML("""<br/>"""),
            FormActions(
                Submit('submit', 'Save', css_class='btn-default'),
                Reset('reset', 'Reset', css_class='btn-warning')
            )
        )

        super(IndicatorForm, self).__init__(*args, **kwargs)
        
        #override the program queryset to use request.user for country
        countries = getCountry(self.request.user)
        self.fields['program'].queryset = Program.objects.filter(funding_status="Funded", country__in=countries)





class QuantitativeOutputsForm(forms.ModelForm):

    class Meta:
        model = QuantitativeOutputs
        exclude = ['create_date', 'edit_date']

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-6'
        self.helper.form_error_title = 'Form Errors'
        self.helper.error_text_inline = True
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.form_tag = True
        self.helper.add_input(Submit('submit', 'Save'))

        super(QuantitativeOutputsForm, self).__init__(*args, **kwargs)


class CollectedDataForm(forms.ModelForm):

    class Meta:
        model = CollectedData
        exclude = ['create_date', 'edit_date']

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-6'
        self.helper.form_error_title = 'Form Errors'
        self.helper.error_text_inline = True
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.form_tag = True
        self.helper.add_input(Submit('submit', 'Save'))

        super(CollectedDataForm, self).__init__(*args, **kwargs)

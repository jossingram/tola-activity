from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template import Context, loader
from datetime import date
import os
import urllib2
import json
import unicodedata
from django.http import HttpResponseRedirect
from django.db import models
from models import Indicator, CollectedData
from activitydb.models import QuantitativeOutputs, Community
from activitydb.models import Program, ProjectAgreement
from indicators.forms import IndicatorForm, CollectedDataForm
from django.shortcuts import render_to_response
from django.contrib import messages
from tola.util import getCountry
from tables import IndicatorTable, IndicatorDataTable
from django_tables2 import RequestConfig
from activitydb.forms import FilterForm
from .forms import QuantitativeOutputsForm, IndicatorForm
from django.db.models import Count
from django.db.models import Q
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import View, DetailView


class IndicatorList(ListView):
    """
    indicator List
    """
    model = Indicator
    template_name = 'indicators/indicator_list.html'

    def get(self, request, *args, **kwargs):

        countries = getCountry(request.user)
        getPrograms = Program.objects.all().filter(country__in=countries, funding_status="Funded")

        if int(self.kwargs['pk']) == 0:
            getProgramsIndicator = Program.objects.all().filter(funding_status="Funded", country__in=countries)
            getIndicators = Indicator.objects.select_related().all()
        else:
            getProgramsIndicator = Program.objects.all().filter(id=self.kwargs['pk'])
            getIndicators = Indicator.objects.all().filter(program__id=self.kwargs['pk']).select_related()

        return render(request, self.template_name, {'getIndicators': getIndicators, 'getPrograms': getPrograms, 'getProgramsIndicator': getProgramsIndicator})


class IndicatorCreate(CreateView):
    """
    indicator Form
    """
    model = Indicator
    template_name = 'indicators/indicator_form.html'

    def get_context_data(self, **kwargs):
        context = super(IndicatorCreate, self).get_context_data(**kwargs)
        context.update({'id': self.kwargs['id']})
        return context

    def dispatch(self, request, *args, **kwargs):
        return super(IndicatorCreate, self).dispatch(request, *args, **kwargs)

    # add the request to the kwargs
    def get_form_kwargs(self):
        kwargs = super(IndicatorCreate, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Success, Indicator Created!')
        form = ""
        return self.render_to_response(self.get_context_data(form=form))


    form_class = IndicatorForm


class IndicatorUpdate(UpdateView):
    """
    indicator Form
    """
    model = Indicator
    template_name = 'indicators/indicator_form.html'


    def get_context_data(self, **kwargs):
        context = super(IndicatorUpdate, self).get_context_data(**kwargs)
        context.update({'id': self.kwargs['pk']})
        return context

    # add the request to the kwargs
    def get_form_kwargs(self):
        kwargs = super(IndicatorUpdate, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid Form', fail_silently=False)
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Success, Indicator Updated!')

        return self.render_to_response(self.get_context_data(form=form))

    form_class = IndicatorForm


class IndicatorDelete(DeleteView):
    """
    indicator Delete
    """
    model = Indicator
    success_url = '/'

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):

        form.save()

        messages.success(self.request, 'Success, Data Deleted!')
        return self.render_to_response(self.get_context_data(form=form))

    form_class = IndicatorForm


def indicatorReport(request, program=0):
    """
    Show LIST of indicators with a filtered search view using django-tables2
    and django-filter
    """
    countries = getCountry(request.user)
    getPrograms = Program.objects.all().filter(funding_status="Funded", country__in=countries)

    if int(program) == 0:
        getIndicators = Indicator.objects.all().select_related()
    else:
        getIndicators = Indicator.objects.all().filter(program__id=program).select_related()

    table = IndicatorTable(getIndicators)
    table.paginate(page=request.GET.get('page', 1), per_page=20)

    if request.method == "GET" and "search" in request.GET:
        #list1 = list()
        #for obj in filtered:
        #    list1.append(obj)
        """
         fields = (indicator_type, name, number, source, definition, disaggregation, baseline, lop_target, means_of_verification, data_collection_method, responsible_person,
                    method_of_analysis, information_use, reporting_frequency, comments, program, sector, approved_by, approval_submitted_by, create_date, edit_date)
        """
        queryset = Indicator.objects.filter(
                                           Q(indicator_type__icontains=request.GET["search"]) |
                                           Q(name__icontains=request.GET["search"]) |
                                           Q(number__icontains=request.GET["search"]) |
                                           Q(definition__startswith=request.GET["search"])
                                          )
        table = IndicatorTable(queryset)

    RequestConfig(request).configure(table)

    # send the keys and vars from the json data to the template along with submitted feed info and silos for new form
    return render(request, "indicators/report.html", {'get_agreements': table, 'getPrograms': getPrograms, 'form': FilterForm(), 'helper': FilterForm.helper})


def programIndicatorReport(request, program=0):
    """
    Show LIST of indicators with a filtered search view using django-tables2
    and django-filter
    """
    program = int(program)
    countries = getCountry(request.user)
    getPrograms = Program.objects.all().filter(funding_status="Funded", country__in=countries)
    getIndicators = Indicator.objects.all().filter(program__id=program).select_related().order_by('indicator_type', 'number')
    getProgram = Program.objects.get(id=program)

    if request.method == "GET" and "search" in request.GET:
        #list1 = list()
        #for obj in filtered:
        #    list1.append(obj)
        """
         fields = (indicator_type, name, number, source, definition, disaggregation, baseline, lop_target, means_of_verification, data_collection_method, responsible_person,
                    method_of_analysis, information_use, reporting_frequency, comments, program, sector, approved_by, approval_submitted_by, create_date, edit_date)
        """
        getIndicators = Indicator.objects.all().filter(
                                           Q(indicator_type__icontains=request.GET["search"]) |
                                           Q(name__icontains=request.GET["search"]) |
                                           Q(number__icontains=request.GET["search"]) |
                                           Q(definition__startswith=request.GET["search"])
                                          ).filter(program__id=program).select_related().order_by('indicator_type','number')


    # send the keys and vars from the json data to the template along with submitted feed info and silos for new form
    return render(request, "indicators/grid_report.html", {'getIndicators': getIndicators, 'getPrograms': getPrograms, 'getProgram': getProgram, 'form': FilterForm(), 'helper': FilterForm.helper})


def indicatorDataReport(request, id=0, program=0, agreement=0):
    """
    Show LIST of indicator based quantitative outputs with a filtered search view using django-tables2
    and django-filter
    """
    countries = getCountry(request.user)
    getPrograms = Program.objects.all().filter(funding_status="Funded", country__in=countries)
    getAgreements = ProjectAgreement.objects.all()
    getIndicators = Indicator.objects.select_related()

    if int(id) != 0:
        getQuantitativeData = QuantitativeOutputs.objects.all().filter(indicator__id = id).select_related()
        getCommunity = Community.objects.all()
        print "id"
    else:
        getQuantitativeData = QuantitativeOutputs.objects.all().select_related()
        getCommunity = Community.objects.all().select_related()

    if int(program) != 0:
        getQuantitativeData = QuantitativeOutputs.objects.all().filter(agreement__program__id = program).select_related()
        getCommunity = Community.objects.all().filter(q_agreement__program__id = program).select_related()

    if int(agreement) != 0:
        getQuantitativeData = QuantitativeOutputs.objects.all().filter(agreement__id = agreement).select_related()
        getCommunity = Community.objects.all().filter(q_agreement__id = agreement).select_related()


    table = IndicatorDataTable(getQuantitativeData)
    table.paginate(page=request.GET.get('page', 1), per_page=20)

    if request.method == "GET" and "search" in request.GET:
        print "search"
        #list1 = list()
        #for obj in filtered:
        #    list1.append(obj)
        """
         fields = ('targeted', 'achieved', 'description', 'indicator', 'agreement', 'complete')
        """
        queryset = QuantitativeOutputs.objects.filter(
                                           Q(agreement__project_name__contains=request.GET["search"]) |
                                           Q(description__icontains=request.GET["search"]) |
                                           Q(indicator__name__contains=request.GET["search"])
                                          ).select_related()
        table = IndicatorDataTable(queryset)

    RequestConfig(request).configure(table)

    # send the keys and vars from the json data to the template along with submitted feed info and silos for new form
    return render(request, "indicators/data_report.html", {'getQuantitativeData':getQuantitativeData,'countries':countries, 'getCommunity':getCommunity, 'table': table, 'getAgreements': getAgreements,'getPrograms':getPrograms, 'getIndicators': getIndicators, 'form': FilterForm(), 'helper': FilterForm.helper, 'id': id,'program':program,'agreement':agreement})


class QuantitativeOutputsList(ListView):
    """
    QuantitativeOutput List
    """
    model = QuantitativeOutputs
    template_name = 'indicators/quantitative_list.html'


    def get(self, request, *args, **kwargs):

        countries = getCountry(request.user)
        getPrograms = Program.objects.all().filter(country__in=countries, funding_status="Funded")
        project_proposal_id = self.kwargs['pk']

        if int(self.kwargs['pk']) == 0:
            getQuantitativeOutputs = QuantitativeOutputs.objects.all().order_by('agreement__program__name','indicator__number')
        else:
            getQuantitativeOutputs = QuantitativeOutputs.objects.all().filter(agreement__program__id=self.kwargs['pk']).order_by('indicator__number')

        return render(request, self.template_name, {'getQuantitativeOutputs': getQuantitativeOutputs, 'project_proposal_id': project_proposal_id, 'getPrograms': getPrograms})


class QuantitativeOutputsCreate(CreateView):
    """
    QuantitativeOutput Form
    """
    model = QuantitativeOutputs
    template_name = 'indicators/quantitativeoutputs_form.html'

    def get_context_data(self, **kwargs):
        context = super(QuantitativeOutputsCreate, self).get_context_data(**kwargs)
        context.update({'id': self.kwargs['id']})
        return context

    # add the request to the kwargs
    def get_form_kwargs(self):
        kwargs = super(QuantitativeOutputsCreate, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def dispatch(self, request, *args, **kwargs):
        return super(QuantitativeOutputsCreate, self).dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = {
            'agreement': self.kwargs['id'],
            }

        return initial

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Success, Quantitative Output Created!')
        form = ""
        return self.render_to_response(self.get_context_data(form=form))


    form_class = QuantitativeOutputsForm


class QuantitativeOutputsUpdate(UpdateView):
    """
    QuantitativeOutput Form
    """
    model = QuantitativeOutputs
    template_name = 'indicators/quantitativeoutputs_form.html'


    def get_context_data(self, **kwargs):
        context = super(QuantitativeOutputsUpdate, self).get_context_data(**kwargs)
        context.update({'id': self.kwargs['pk']})
        return context

    # add the request to the kwargs
    def get_form_kwargs(self):
        kwargs = super(QuantitativeOutputsUpdate, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid Form', fail_silently=False)
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Success, Quantitative Output Updated!')

        return self.render_to_response(self.get_context_data(form=form))

    form_class = QuantitativeOutputsForm


class QuantitativeOutputsDelete(DeleteView):
    """
    QuantitativeOutput Delete
    """
    model = QuantitativeOutputs
    success_url = '/'

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):

        form.save()

        messages.success(self.request, 'Success, Quantitative Output Deleted!')
        return self.render_to_response(self.get_context_data(form=form))

    form_class = QuantitativeOutputsForm


class CollectedDataList(ListView):
    """
    CollectedData List
    """
    model = CollectedData
    template_name = 'indicators/collecteddata_list.html'

    def get(self, request, *args, **kwargs):

        countries = getCountry(request.user)
        getPrograms = Program.objects.all().filter(country__in=countries, funding_status="Funded")

        if int(self.kwargs['pk']) == 0:
            getCollectedData = CollectedData.objects.all()
        else:
            getCollectedData = CollectedData.objects.all().filter(program__id=self.kwargs['pk'])

        return render(request, self.template_name, {'getCollectedData': getCollectedData, 'getPrograms': getPrograms})


class CollectedDataCreate(CreateView):
    """
    CollectedData Form
    """
    model = CollectedData
    template_name = 'indicators/collecteddata_form.html'

    def get_context_data(self, **kwargs):
        context = super(CollectedDataCreate, self).get_context_data(**kwargs)
        context.update({'program': self.kwargs['program']})
        context.update({'indicator': self.kwargs['indicator']})
        return context

    def dispatch(self, request, *args, **kwargs):
        return super(CollectedDataCreate, self).dispatch(request, *args, **kwargs)

    # add the request to the kwargs
    def get_form_kwargs(self):
        kwargs = super(CollectedDataCreate, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Success, Data Created!')
        form = ""
        return self.render_to_response(self.get_context_data(form=form))


    form_class = CollectedDataForm


class CollectedDataUpdate(UpdateView):
    """
    CollectedData Form
    """
    model = CollectedData
    template_name = 'indicators/collecteddata_form.html'


    def get_context_data(self, **kwargs):
        context = super(CollectedDataUpdate, self).get_context_data(**kwargs)
        context.update({'id': self.kwargs['pk']})
        return context

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid Form', fail_silently=False)
        return self.render_to_response(self.get_context_data(form=form))

    # add the request to the kwargs
    def get_form_kwargs(self):
        kwargs = super(CollectedDataUpdate, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Success, Data Updated!')

        return self.render_to_response(self.get_context_data(form=form))

    form_class = CollectedDataForm


class CollectedDataDelete(DeleteView):
    """
    CollectedData Delete
    """
    model = CollectedData
    success_url = '/'

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):

        form.save()

        messages.success(self.request, 'Success, Data Deleted!')
        return self.render_to_response(self.get_context_data(form=form))

    form_class = CollectedDataForm


def tool(request):

    return render(request, 'indicators/tool.html')


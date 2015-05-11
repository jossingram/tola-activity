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
from activitydb.models import QuantitativeOutputs
from activitydb.models import Program
from indicators.forms import IndicatorForm, CollectedDataForm
from django.shortcuts import render_to_response
from django.contrib import messages
from tola.util import getCountry
from tables import IndicatorTable, IndicatorDataTable
from django_tables2 import RequestConfig
from activitydb.forms import FilterForm
from .forms import QuantitativeOutputsForm
from django.db.models import Count
from django.db.models import Q
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import View, DetailView


def home(request, id):
    """
    Get all of the Programs
    """
    #set country to afghanistan for now until we have user data on country
    #use self.request.user to get users country
    #self.kwargs.pk = ID of program from dropdown
    countries = getCountry(request.user)
    getPrograms = Program.objects.all().filter(funding_status="Funded", country__in=countries)
    print int(id)
    if int(id) != 0:
        getIndicators = Indicator.objects.all().filter(program__id=id)
    else:
        getIndicators = Indicator.objects.all()
    return render(request, 'indicators/home.html',{'getPrograms':getPrograms, 'getIndicators': getIndicators})

def dashboard(request):

    return render(request, 'indicators/dashboard.html')

def indicator(request):
    """
    Create an Indicator
    """
    if request.method == 'POST': # If the form has been submitted...
        form = IndicatorForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # save data to read
            new = form.save()
            messages.success(request, 'Success, Indicator Created!')
            return HttpResponseRedirect('/indicators/indicator') # Redirect after POST to getLogin
    else:
        form = IndicatorForm() # An unbound form

    return render(request, 'indicators/indicator.html', {'form': form,})

def editIndicator(request,id):
    """
    Edit an Indicator
    """
    if request.method == 'POST': # If the form has been submitted...
        form = IndicatorForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # save data to read
            update = Indicator.objects.get(pk=id)
            form = IndicatorForm(request.POST, instance=update)
            new = form.save(commit=True)
            messages.success(request, 'Success, Indicator Saved!')
            return HttpResponseRedirect('/indicators/editIndicator/' + id)
        else:
            print "not valid"
    else:
        value= get_object_or_404(Indicator, pk=id)
        form = IndicatorForm(instance=value) # An unbound form

    return render(request, 'indicators/indicator.html', {'form': form,'value':value})



def programIndicator(request,id):
    """
    View the indicators for a program
    """
    IndicatorFormSet = modelformset_factory(Indicator,extra=0)
    formset = IndicatorFormSet(queryset=Indicator.objects.all().filter(program__id=id))

    if request.method == 'POST':
        #deal with posting the data
        formset = IndicatorFormSet(request.POST)
        if formset.is_valid():
            #if it is not valid then the "errors" will fall through and be returned
            formset.save()
        return HttpResponseRedirect('/indicators/programIndicator/' + id)

    return render(request, 'indicators/programIndicator.html', {'formset': formset})

def editProgram(request,id):
    """
    Edit a program
    """
    if request.method == 'POST': # If the form has been submitted...
        form = ProgramForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # save data to read
            update = Program.objects.get(pk=id)
            form = ProgramForm(request.POST, instance=update)
            new = form.save(commit=True)
            return HttpResponseRedirect('indicators/editProgram/' + id)
        else:
            print "not valid"
    else:
        value= get_object_or_404(Program, pk=id)
        form = ProgramForm(instance=value) # An unbound form

    return render(request, 'indicators/program.html', {'form': form,'value':value})


def indicatorReport(request):
    """
    Show LIST of submitted incidents with a filtered search view using django-tables2
    and django-filter
    """
    countries = getCountry(request.user)
    getPrograms = Program.objects.all().filter(funding_status="Funded", country__in=countries)
    getIndicators = Indicator.objects.select_related()
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
    return render(request, "indicators/report.html", {'get_agreements': table, 'program': getPrograms, 'form': FilterForm(), 'helper': FilterForm.helper})


def indicatorDataReport(request,id):
    """
    Show LIST of submitted incidents with a filtered search view using django-tables2
    and django-filter
    """
    countries = getCountry(request.user)
    getPrograms = Program.objects.all().filter(funding_status="Funded", country__in=countries)
    getIndicators = Indicator.objects.select_related()
    if int(id) != 0:
        getQuantitativeData = QuantitativeOutputs.objects.all().filter(logframe_indicator__id = id).select_related()
    else:
        getQuantitativeData = QuantitativeOutputs.objects.all().select_related()
    table = IndicatorDataTable(getQuantitativeData)
    table.paginate(page=request.GET.get('page', 1), per_page=20)

    if request.method == "GET" and "search" in request.GET:
        #list1 = list()
        #for obj in filtered:
        #    list1.append(obj)
        """
         fields = ('targeted', 'achieved', 'description', 'logframe_indicator', 'non_logframe_indicator', 'agreement', 'complete')
        """
        queryset = QuantitativeOutputs.objects.filter(
                                           Q(agreement__project_name__contains=request.GET["search"]) |
                                           Q(description__icontains=request.GET["search"]) |
                                           Q(logframe_indicator__name__contains=request.GET["search"]) |
                                           Q(non_logframe_indicator__contains=request.GET["search"])
                                          ).select_related()
        table = IndicatorDataTable(queryset)

    RequestConfig(request).configure(table)

    # send the keys and vars from the json data to the template along with submitted feed info and silos for new form
    return render(request, "indicators/data_report.html", {'get_agreements': table, 'getIndicators': getIndicators, 'form': FilterForm(), 'helper': FilterForm.helper})


class QuantitativeOutputsList(ListView):
    """
    QuantitativeOutput List
    """
    model = QuantitativeOutputs
    template_name = 'indicators/quantitative_list.html'

    def get(self, request, *args, **kwargs):

        project_proposal_id = self.kwargs['pk']

        if int(self.kwargs['pk']) == 0:
            getQuantitativeOutputs = QuantitativeOutputs.objects.all()
        else:
            getQuantitativeOutputs = QuantitativeOutputs.objects.all().filter(project_proposal_id=self.kwargs['pk'])

        return render(request, self.template_name, {'getQuantitativeOutputs': getQuantitativeOutputs, 'project_proposal_id': project_proposal_id})


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

        if int(self.kwargs['pk']) == 0:
            getCollectedData = CollectedData.objects.all()
        else:
            getCollectedData = CollectedData.objects.all().filter(project_proposal_id=self.kwargs['pk'])

        return render(request, self.template_name, {'getCollectedData': getCollectedData})


class CollectedDataCreate(CreateView):
    """
    CollectedData Form
    """
    model = CollectedData
    template_name = 'indicators/collecteddata_form.html'

    def get_context_data(self, **kwargs):
        context = super(CollectedDataCreate, self).get_context_data(**kwargs)
        context.update({'id': self.kwargs['id']})
        return context

    def dispatch(self, request, *args, **kwargs):
        return super(CollectedDataCreate, self).dispatch(request, *args, **kwargs)


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


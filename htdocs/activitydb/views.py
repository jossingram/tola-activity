from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import View, DetailView
from .models import ProjectProposal, ProgramDashboard, Program, Country, Province, Village, District, ProjectAgreement, ProjectComplete, Community, Documentation, Monitor, Benchmarks, TrainingAttendance, Beneficiary, QuantitativeOutputs, Budget
from silo.models import Silo, ValueStore, DataField
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.utils import timezone
from .forms import ProjectProposalForm, ProgramDashboardForm, ProjectAgreementForm, ProjectAgreementCreateForm, ProjectCompleteForm, DocumentationForm, CommunityForm, MonitorForm, BenchmarkForm, TrainingAttendanceForm, BeneficiaryForm, QuantitativeOutputsForm, BudgetForm, FilterForm
import logging
from django.shortcuts import render
from django.contrib import messages
from django.db import connections
from django.contrib.auth.models import User
from django.db.models import Count
from django.db.models import Q
from django.contrib.auth.decorators import permission_required
from tables import ProjectAgreementTable
from django_tables2 import RequestConfig
from filters import ProjectAgreementFilter
from datetime import datetime
import json
from django.shortcuts import get_object_or_404

from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse, HttpResponseRedirect

# Get an instance of a logger
logger = logging.getLogger(__name__)

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from tola.util import getCountry
from mixins import AjaxableResponseMixin
"""
project_proposal_id is the key to link each related form
ProjectProposal, ProjectAgreement, ProjectComplete, Community (Main Forms and Workflow)
Monitor, Benchmark, TrainingAttendance and Beneficiary are related to Project Agreement via
the project_agreement_id

TO-DO: Create imports for Agreement, Community, and Training Attendance
TO-DO: Update ProjectProposal IMport with new form fields
TO-DO: Beneficiaries List, Form and Delete
"""


def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj

def group_required(*group_names, **url):
    #Requires user membership in at least one of the groups passed in.
    def in_groups(u):
        if u.is_authenticated():
            if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
                return True
        return False
    return user_passes_test(in_groups)


class ProjectDash(ListView):

    template_name = 'activitydb/projectdashboard_list.html'

    def get(self, request, *args, **kwargs):
        countries = getCountry(request.user)
        getPrograms = Program.objects.all().filter(funding_status="Funded", country__in=countries)
        form = ProgramDashboardForm

        if int(self.kwargs['pk']) == 0:
            getDashboard = ProgramDashboard.objects.all()
            getDocumentCount = 0
            getCommunityCount = 0
            getTrainingCount = 0
        else:
            getDashboard = ProgramDashboard.objects.all().filter(project_proposal__id=self.kwargs['pk'])

            getDocumentCount = Documentation.objects.all().filter(project__id=self.kwargs['pk']).count()
            getCommunityCount = Community.objects.all().filter(projectproposal__id=self.kwargs['pk']).count()
            getTrainingCount = TrainingAttendance.objects.all().filter(project_proposal_id=self.kwargs['pk']).count()

        if int(self.kwargs['pk']) == 0:
            getProgram =Program.objects.all().filter(funding_status="Funded", country__in=countries)
        else:
            getProgram =Program.objects.get(proposal__id=self.kwargs['pk'])

        return render(request, self.template_name, {'form': form, 'getProgram': getProgram, 'getDashboard': getDashboard,
                                                    'getPrograms':getPrograms, 'getDocumentCount':getDocumentCount,
                                                    'getCommunityCount':getCommunityCount, 'getTrainingCount':getTrainingCount})


class ProgramDash(ListView):
    """
    Dashboard links for and status for each program with number of proposals and
    agreements and complete from the dashboard model
    :param request:
    :param pk: program_id
    :return:
    """
    template_name = 'activitydb/programdashboard_list.html'

    def get(self, request, *args, **kwargs):
        countries = getCountry(request.user)
        getPrograms = Program.objects.all().filter(funding_status="Funded", country__in=countries)

        form = ProgramDashboardForm

        if int(self.kwargs['pk']) == 0:
            getDashboard = Program.objects.all().filter(funding_status="Funded", country__in=countries).filter(Q(agreement__isnull=False) | Q(proposal__isnull=False) | Q(complete__isnull=False)).order_by('name').values('id', 'name', 'gaitid','agreement__id','proposal__id','complete__id')

        else:
            getDashboard = Program.objects.all().filter(id=self.kwargs['pk'], funding_status="Funded", country__in=countries).filter(Q(agreement__isnull=False) | Q(proposal__isnull=False) | Q(complete__isnull=False)).order_by('name').values('id', 'name', 'gaitid','agreement__id','proposal__id','complete__id')

        return render(request, self.template_name, {'form': form, 'getDashboard': getDashboard, 'getPrograms':getPrograms})


class ProjectProposalList(ListView):
    """
    Project Proposal
    list of proposals submitted and associated with the dashboard model
    :param request:
    :param pk: program_id
    :return:
    """
    model = ProjectProposal
    template_name = 'activitydb/projectproposal_list.html'

    def get(self, request, *args, **kwargs):
        form = ProgramDashboardForm
        countries = getCountry(request.user)
        getPrograms = Program.objects.all().filter(funding_status="Funded", country__in=countries)

        if int(self.kwargs['pk']) == 0:
            getDashboard = ProjectProposal.objects.all().filter(program__country__in=countries)
            return render(request, self.template_name, {'form': form, 'getDashboard':getDashboard,'getPrograms':getPrograms})
        else:
            getDashboard = ProjectProposal.objects.all().filter(program__id=self.kwargs['pk'])
            getProgram =Program.objects.get(id=self.kwargs['pk'])

            return render(request, self.template_name, {'form': form, 'getProgram': getProgram, 'getDashboard':getDashboard,'getPrograms':getPrograms})


class ProjectProposalImport(ListView):
    """
    Import project proposal from a Tola data source Silo
    """
    model = Silo

    def get_context_data(self, **kwargs):
        context = super(ProjectProposalImport, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

    template_name = 'activitydb/projectproposal_import.html'


class ProjectProposalCreate(CreateView):
    """
    Project Proposal Form
    :param request:
    :param id: program_id
    """
    model = ProjectProposal

    # add the request to the kwargs
    def get_form_kwargs(self):
        kwargs = super(ProjectProposalCreate, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    #get shared data from project agreement and pre-populate form with it
    def get_initial(self):
        initial = {
            'approved_by': self.request.user,
            'approval_submitted_by': self.request.user,
            }

        return initial

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):

        form.save()

        #create a new dashbaord entry for the project
        latest = ProjectProposal.objects.latest('id')
        getProposal = ProjectProposal.objects.get(id=latest.id)
        getProgram = Program.objects.get(id=latest.program_id)

        create_dashboard_entry = ProgramDashboard(program=getProgram, project_proposal=getProposal)
        create_dashboard_entry.save()

        messages.success(self.request, 'Success, Proposal Created!')
        redirect_url = '/activitydb/projectproposal_update/' + str(latest.id)
        return HttpResponseRedirect(redirect_url)

    form_class = ProjectProposalForm


class ProjectProposalUpdate(UpdateView):
    """
    Project Proposal Form
    :param request:
    :param id: project_proposal_id
    """
    model = ProjectProposal

    def get_context_data(self, **kwargs):
        context = super(ProjectProposalUpdate, self).get_context_data(**kwargs)
        getProposal = ProjectProposal.objects.get(id=self.kwargs['pk'])
        id = getProposal.id
        context.update({'id': id})
        return context

    # add the request to the kwargs
    def get_form_kwargs(self):
        kwargs = super(ProjectProposalUpdate, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    #get shared data from project agreement and pre-populate form with it
    def get_initial(self):
        initial = {
            'approved_by': self.request.user,
            'approval_submitted_by': self.request.user,
            }

        return initial

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):

        form.save()
        messages.success(self.request, 'Success, Proposal Updated!')

        is_approved = self.request.GET.get('approved')

        if is_approved:
            update_dashboard = ProgramDashboard.objects.filter(project_proposal__id=self.request.GET.get('id')).update(project_proposal_approved=True)

        return self.render_to_response(self.get_context_data(form=form))

    form_class = ProjectProposalForm


class ProjectProposalDelete(DeleteView):
    """
    Project Proposal Delete
    """
    model = ProjectProposal
    success_url = '/activitydb/projectproposal_list/0/'

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):

        form.save()

        messages.success(self.request, 'Success, Proposal Deleted!')

        return self.render_to_response(self.get_context_data(form=form))

    form_class = ProjectProposalForm


class ProjectProposalDetail(DetailView):

    model = ProjectProposal
    context_object_name = 'proposal'
    queryset = ProjectProposal.objects.all()

    def get_context_data(self, **kwargs):
        context = super(ProjectProposalDetail, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        data = ProjectProposal.objects.all().filter(id=self.kwargs['pk'])
        getData = serializers.serialize('python', data)
        #return just the fields and skip the object name
        justFields = [d['fields'] for d in getData]
        #handle date exceptions with date_handler
        jsonData =json.dumps(justFields, default=date_handler)
        context.update({'jsonData': jsonData})
        context.update({'id': self.kwargs['pk']})

        return context


class ProjectAgreementList(ListView):
    """
    Project Agreement
    :param request:
    :param id: project_proposal_id
    """
    model = ProjectAgreement
    template_name = 'activitydb/projectagreement_list.html'

    def get(self, request, *args, **kwargs):
        form = ProgramDashboardForm
        countries = getCountry(request.user)
        getPrograms = Program.objects.all().filter(funding_status="Funded", country__in=countries)

        if int(self.kwargs['pk']) == 0:
            getDashboard = ProjectAgreement.objects.all()
            return render(request, self.template_name, {'form': form, 'getDashboard':getDashboard,'getPrograms':getPrograms})
        else:
            getDashboard = ProjectAgreement.objects.all().filter(program__id=self.kwargs['pk'])
            getProgram =Program.objects.get(id=self.kwargs['pk'])

            return render(request, self.template_name, {'form': form, 'getProgram': getProgram, 'getDashboard':getDashboard,'getPrograms':getPrograms})


class ProjectAgreementImport(ListView):
    """
    Import a project agreement from Tola source Silo
    """
    model = Silo

    def get_context_data(self, **kwargs):
        context = super(ProjectAgreementImport, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

    template_name = 'activitydb/projectagreement_import.html'


class ProjectAgreementCreate(CreateView):
    """
    Project Agreement Form
    :param request:
    :param id: project_proposal_id
    """
    model = ProjectAgreement
    template_name = 'activitydb/projectagreement_form.html'

     # add the request to the kwargs
    def get_form_kwargs(self):
        kwargs = super(ProjectAgreementCreate, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    #get shared data from project agreement and pre-populate form with it
    def get_initial(self):
        getProjectProposal = ProjectProposal.objects.get(id=self.kwargs['pk'])

        pre_initial = {
            'approved_by': self.request.user,
            'estimated_by': self.request.user,
            'checked_by': self.request.user,
            'reviewed_by': self.request.user,
            'approval_submitted_by': self.request.user,
            'program': getProjectProposal.program,
            'project_proposal': getProjectProposal.id,
            'project_name': getProjectProposal.project_name,
            'proposal_num': getProjectProposal.proposal_num,
            'activity_code': getProjectProposal.activity_code,
            'office': getProjectProposal.office,
            'estimated_by': getProjectProposal.estimated_by,
            'sector': getProjectProposal.sector,
            'project_activity': getProjectProposal.project_activity,
            'project_type': getProjectProposal.project_type,
            }

        try:
            getCommunites = Community.objects.filter(projectproposal__id=self.kwargs['pk']).values_list('id',flat=True)
            communites = {'community': [o for o in getCommunites],}
            initial = pre_initial.copy()
            initial.update(communites)
        except Community.DoesNotExist:
            getCommunites = None

        return initial

    def get_context_data(self, **kwargs):
        context = super(ProjectAgreementCreate, self).get_context_data(**kwargs)
        getProposal = ProjectProposal.objects.get(id=self.kwargs['pk'])
        id = getProposal.id
        context.update({'id': id})

        return context

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):

        form.save()

        #save formset from context
        context = self.get_context_data()

        latest = ProjectAgreement.objects.latest('id')
        getAgreement = ProjectAgreement.objects.get(id=latest.id)

        update_dashboard = ProgramDashboard.objects.filter(project_proposal__id=self.request.POST['project_proposal']).update(project_agreement=getAgreement)

        messages.success(self.request, 'Success, Agreement Created!')
        redirect_url = '/activitydb/projectagreement_update/' + str(latest.id)
        return HttpResponseRedirect(redirect_url)

    form_class = ProjectAgreementCreateForm


class ProjectAgreementUpdate(UpdateView):
    """
    Project Agreement Form
    :param request:
    :param id: project_agreement_id
    """
    model = ProjectAgreement

    def get_context_data(self, **kwargs):
        context = super(ProjectAgreementUpdate, self).get_context_data(**kwargs)
        getAgreement = ProjectAgreement.objects.get(id=self.kwargs['pk'])
        id = getAgreement.project_proposal_id
        context.update({'id': id})
        try:
            getQuantitative = QuantitativeOutputs.objects.all().filter(agreement__id=self.kwargs['pk'])
        except QuantitativeOutputs.DoesNotExist:
            getQuantitative = None
        context.update({'getQuantitative': getQuantitative})

        try:
            getMonitor = Monitor.objects.all().filter(agreement__id=self.kwargs['pk'])
        except Monitor.DoesNotExist:
            getMonitor = None
        context.update({'getMonitor': getMonitor})

        try:
            getBenchmark = Benchmarks.objects.all().filter(agreement__id=self.kwargs['pk'])
        except Benchmarks.DoesNotExist:
            getBenchmark = None
        context.update({'getBenchmark': getBenchmark})

        try:
            getBudget = Budget.objects.all().filter(agreement__id=self.kwargs['pk'])
        except Budget.DoesNotExist:
            getBudget = None
        context.update({'getBudget': getBudget})

        return context

    # add the request to the kwargs
    def get_form_kwargs(self):
        kwargs = super(ProjectAgreementUpdate, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    #get shared data from project agreement and pre-populate form with it
    def get_initial(self):
        getProjectProposal = ProjectProposal.objects.get(projectagreement__id=self.kwargs['pk'])

        initial = {
            'approved_by': self.request.user,
            'estimated_by': self.request.user,
            'checked_by': self.request.user,
            'reviewed_by': self.request.user,
            'approval_submitted_by': self.request.user,
            'program': getProjectProposal.program,
            'project_proposal': getProjectProposal.id,
            'project_name': getProjectProposal.project_name,
            'proposal_num': getProjectProposal.proposal_num,
            'activity_code': getProjectProposal.activity_code,
            'office': getProjectProposal.office,
            'estimated_by': getProjectProposal.estimated_by,
            'sector': getProjectProposal.sector,
            'project_activity': getProjectProposal.project_activity,
            'project_type': getProjectProposal.project_type,
            }

        try:
            getCommunites = Community.objects.get(projectproposal__id=self.kwargs['pk'])
            communites = {'community': [o for o in getCommunites.name],}
            initial = initial + communites
        except Community.DoesNotExist:
            getCommunites = None

        return initial

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):

        form.save()
        #save formset from context
        context = self.get_context_data()
        budget_form = context['budget_form']
        self.object = form.save()
        budget_form.instance = self.object
        budget_form.save()

        messages.success(self.request, 'Success, form updated!')

        return self.render_to_response(self.get_context_data(form=form))

    form_class = ProjectAgreementForm


class ProjectAgreementDetail(DetailView):

    model = ProjectAgreement
    context_object_name = 'agreement'
    queryset = ProjectAgreement.objects.all()


    def get_object(self, queryset=ProjectAgreement.objects.all()):
        try:
            return queryset.get(project_proposal__id=self.kwargs['pk'])
        except ProjectAgreement.DoesNotExist:
            return None

    def get_context_data(self, **kwargs):
        context = super(ProjectAgreementDetail, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        data = ProjectAgreement.objects.all().filter(project_proposal__id=self.kwargs['pk'])
        getData = serializers.serialize('python', data)
        #return just the fields and skip the object name
        justFields = [d['fields'] for d in getData]
        #handle date exceptions with date_handler
        jsonData =json.dumps(justFields, default=date_handler)
        context.update({'jsonData': jsonData})

        context.update({'id': self.kwargs['pk']})

        return context


class ProjectAgreementDelete(DeleteView):
    """
    Project Agreement Delete
    """
    model = ProjectAgreement
    success_url = '/activitydb/projectagreement_list/0/'

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):

        form.save()

        return HttpResponseRedirect('/activitydb/success')

    form_class = ProjectAgreementForm


class ProjectCompleteList(ListView):
    """
    Project Complete
    :param request:
    :param pk: program_id
    """
    model = ProjectComplete
    template_name = 'activitydb/projectcomplete_list.html'

    def get(self, request, *args, **kwargs):
        form = ProgramDashboardForm
        countries = getCountry(request.user)
        getPrograms = Program.objects.all().filter(funding_status="Funded", country__in=countries)

        if int(self.kwargs['pk']) == 0:
            getDashboard = ProjectAgreement.objects.all()
            return render(request, self.template_name, {'form': form, 'getDashboard':getDashboard,'getPrograms':getPrograms})
        else:
            getDashboard = ProjectAgreement.objects.all().filter(program__id=self.kwargs['pk'])
            getProgram =Program.objects.get(id=self.kwargs['pk'])

            return render(request, self.template_name, {'form': form, 'getProgram': getProgram, 'getDashboard':getDashboard,'getPrograms':getPrograms})


class ProjectCompleteCreate(CreateView):
    """
    Project Complete Form
    """
    model = ProjectComplete
    template_name = 'activitydb/projectcomplete_form.html'

    # add the request to the kwargs
    def get_form_kwargs(self):
        kwargs = super(ProjectCompleteCreate, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    #get shared data from project agreement and pre-populate form with it
    def get_initial(self):
        getProjectAgreement = ProjectAgreement.objects.get(id=self.kwargs['pk'])
        initial = {
            'approved_by': self.request.user,
            'approval_submitted_by': self.request.user,
            'program': getProjectAgreement.program,
            'project_proposal': getProjectAgreement.project_proposal,
            'project_agreement': getProjectAgreement.id,
            'project_name': getProjectAgreement.project_name,
            'activity_code': getProjectAgreement.activity_code,
            'expected_start_date': getProjectAgreement.expected_start_date,
            'expected_end_date': getProjectAgreement.expected_end_date,
            'expected_duration': getProjectAgreement.expected_duration,
            'estimated_budget': getProjectAgreement.total_estimated_budget,
        }

        try:
            getCommunites = Community.objects.get(projectproposal__id=self.kwargs['pk'])
            communites = {'community': [o for o in getCommunites.name],}
            initial = initial + communites
        except Community.DoesNotExist:
            getCommunites = None

        return initial

    def get_context_data(self, **kwargs):
        context = super(ProjectCompleteCreate, self).get_context_data(**kwargs)
        getAgreement = ProjectAgreement.objects.get(id=self.kwargs['pk'])
        id = getAgreement.project_proposal_id
        context.update({'id': id})

        return context

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):

        form.save()
        context = self.get_context_data()
        budget_form = context['budget_form']
        self.object = form.save()
        budget_form.instance = self.object
        budget_form.save()

        latest = ProjectComplete.objects.latest('id')
        getComplete = ProjectComplete.objects.get(id=latest.id)

        ProgramDashboard.objects.filter(project_proposal__id=self.request.POST['project_proposal']).update(project_completion=getComplete)

        messages.success(self.request, 'Success, Completion Form Created!')
        redirect_url = '/activitydb/projectcomplete_update/' + str(latest.id)
        return HttpResponseRedirect(redirect_url)

    form_class = ProjectCompleteForm


class ProjectCompleteUpdate(UpdateView):
    """
    Project Complete Form
    """
    model = ProjectComplete
    template_name = 'activitydb/projectcomplete_form.html'

    def get_context_data(self, **kwargs):
        context = super(ProjectCompleteUpdate, self).get_context_data(**kwargs)
        getComplete = ProjectComplete.objects.get(id=self.kwargs['pk'])
        id = getComplete.project_proposal_id
        context.update({'id': id})

        #get quantitative data
        try:
            getQuantitative = QuantitativeOutputs.objects.all().filter(complete_id=self.kwargs['pk'])
            #if there aren't any quantitative try importing from the agreement
            if not getQuantitative:
                QuantitativeOutputs.update(complete_id=self.kwargs['pk']).filter(agreement__id=getQuantitative.agreement_id)
        except QuantitativeOutputs.DoesNotExist:
            getQuantitative = None
        context.update({'getQuantitative': getQuantitative})

        #get budget data
        try:
            getBudget = Budget.objects.all().filter(agreement__id=self.kwargs['pk'])
        except Budget.DoesNotExist:
            getBudget = None
        context.update({'getBudget': getBudget})

        return context

    # add the request to the kwargs
    def get_form_kwargs(self):
        kwargs = super(ProjectCompleteUpdate, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    #get shared data from project agreement and pre-populate form with it
    def get_initial(self):
        initial = {
            'approved_by': self.request.user,
            'approval_submitted_by': self.request.user,
        }

        #update quantitative with new agreement
        try:
            getQuantitative = QuantitativeOutputs.objects.all().filter(complete_id=self.kwargs['pk'])
            #if there aren't any quantitative try importing from the agreement
            if not getQuantitative:
                QuantitativeOutputs.update(complete_id=self.kwargs['pk']).filter(agreement__id=getQuantitative.agreement_id)
        except QuantitativeOutputs.DoesNotExist:
            getQuantitative = None

        return initial

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):

        form.save()
        context = self.get_context_data()
        self.object = form.save()

        is_approved = self.request.GET.get('approved')

        if is_approved:
            update_dashboard = ProgramDashboard.objects.filter(project_completion__id=self.request.GET.get('id')).update(project_completion_approved=True)


        messages.success(self.request, 'Success, form updated!')

        return self.render_to_response(self.get_context_data(form=form, request=request))

    form_class = ProjectCompleteForm


class ProjectCompleteDetail(DetailView):

    model = ProjectComplete
    context_object_name = 'complete'

    def get_object(self, queryset=ProjectComplete.objects.all()):
        try:
            return queryset.get(project_proposal__id=self.kwargs['pk'])
        except ProjectComplete.DoesNotExist:
            return None

    def get_context_data(self, **kwargs):

        context = super(ProjectCompleteDetail, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        try:
            data = ProjectComplete.objects.all().filter(project_proposal__id=self.kwargs['pk'])
        except ProjectComplete.DoesNotExist:
            data = None
        getData = serializers.serialize('python', data)
        #return just the fields and skip the object name
        justFields = [d['fields'] for d in getData]
        #temp name fiels
        jsonData =json.dumps(justFields, default=date_handler)
        context.update({'jsonData': jsonData})
        context.update({'id':self.kwargs['pk']})

        return context


class ProjectCompleteDelete(DeleteView):
    """
    Project Complete Delete
    """
    model = ProjectComplete
    success_url = '/activitydb/projectcomplete_list/0/'

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):

        form.save()

        return HttpResponseRedirect('/activitydb/success')

    form_class = ProjectCompleteForm


class ProjectCompleteImport(ListView):

    model = Silo

    def get_context_data(self, **kwargs):
        context = super(ProjectCompleteImport, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

    template_name = 'activitydb/projectcomplete_import.html'


class DocumentationList(ListView):
    """
    Documentation
    """
    model = Documentation
    template_name = 'activitydb/documentation_list.html'

    def get(self, request, *args, **kwargs):

        project_proposal_id = self.kwargs['pk']

        if int(self.kwargs['pk']) == 0:
            getDocumentation = Documentation.objects.all()
        else:
            getDocumentation = Documentation.objects.all().filter(project__id=self.kwargs['pk'])

        return render(request, self.template_name, {'getDocumentation':getDocumentation, 'project_proposal_id': project_proposal_id})


class DocumentationCreate(CreateView):
    """
    Documentation Form
    """
    model = Documentation

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):

        form.save()

        messages.success(self.request, 'Success, Documentation Created!')
        return self.render_to_response(self.get_context_data(form=form))

    form_class = DocumentationForm


class DocumentationUpdate(UpdateView):
    """
    Documentation Form
    """
    model = Documentation

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):

        form.save()
        messages.success(self.request, 'Success, Documentation Updated!')

        return self.render_to_response(self.get_context_data(form=form))

    form_class = DocumentationForm


class DocumentationDelete(DeleteView):
    """
    Documentation Form
    """
    model = Documentation
    success_url = reverse_lazy('documentation_list')

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):

        form.save()

        messages.success(self.request, 'Success, Documentation Deleted!')
        return self.render_to_response(self.get_context_data(form=form))

    form_class = DocumentationForm


class CommunityList(ListView):
    """
    Community
    """
    model = Community
    template_name = 'activitydb/community_list.html'

    def dispatch(self, request, *args, **kwargs):
        if request.GET.has_key('report'):
            template_name = 'activitydb/community_report.html'
        else:
            template_name = 'activitydb/community_list.html'
        return super(CommunityList, self).dispatch(request, *args, **kwargs)


    def get(self, request, *args, **kwargs):
        countries = getCountry(request.user)
        project_proposal_id = self.kwargs['pk']

        if int(self.kwargs['pk']) == 0:
            getCommunity = Community.objects.all()
        else:
            getCommunity = Community.objects.all().filter(projectproposal__id=self.kwargs['pk'])

        return render(request, self.template_name, {'getCommunity':getCommunity,'project_proposal_id': project_proposal_id,'country': countries})


class CommunityReport(ListView):
    """
    Community
    """
    model = Community
    template_name = 'activitydb/community_report.html'


    def get(self, request, *args, **kwargs):
        countries = getCountry(request.user)
        project_proposal_id = self.kwargs['pk']

        if int(self.kwargs['pk']) == 0:
            getCommunity = Community.objects.all()
        else:
            getCommunity = Community.objects.all().filter(projectproposal__id=self.kwargs['pk'])

        id=self.kwargs['pk']

        return render(request, self.template_name, {'getCommunity':getCommunity,'project_proposal_id': project_proposal_id,'id':id,'country': countries})


class CommunityCreate(CreateView):
    """
    Community Form
    """
    model = Community

    @method_decorator(group_required('Editor',url='activitydb/permission'))
    def dispatch(self, request, *args, **kwargs):
        return super(CommunityCreate, self).dispatch(request, *args, **kwargs)

    # add the request to the kwargs
    def get_form_kwargs(self):
        kwargs = super(CommunityCreate, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_initial(self):
        initial = {
            'approved_by': self.request.user,
            'filled_by': self.request.user,
        }

        return initial

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Success, Community Created!')
        return self.render_to_response(self.get_context_data(form=form))

    form_class = CommunityForm


class CommunityUpdate(UpdateView):
    """
    Community Form
    """
    model = Community

    # add the request to the kwargs
    def get_form_kwargs(self):
        kwargs = super(CommunityUpdate, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid Form', fail_silently=False)
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Success, Community Updated!')

        return self.render_to_response(self.get_context_data(form=form))

    form_class = CommunityForm


class CommunityDelete(DeleteView):
    """
    Community Form
    """
    model = Community
    success_url = reverse_lazy('community_list')

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):

        form.save()

        messages.success(self.request, 'Success, Community Deleted!')
        return self.render_to_response(self.get_context_data(form=form))

    form_class = CommunityForm


class MonitorList(ListView):
    """
    Monitoring Data
    """
    model = Monitor
    template_name = 'activitydb/monitor_list.html'

    def get(self, request, *args, **kwargs):

        project_proposal_id = self.kwargs['pk']

        if int(self.kwargs['pk']) == 0:
            getMonitorData = Monitor.objects.all()
        else:
            getMonitorData = Monitor.objects.all().filter(agreement__id=self.kwargs['pk'])

        if int(self.kwargs['pk']) == 0:
            getBenchmarkData = Benchmarks.objects.all()
        else:
            getBenchmarkData = Benchmarks.objects.all().filter(agreement__id=self.kwargs['pk'])

        return render(request, self.template_name, {'getMonitorData': getMonitorData, 'getBenchmarkData': getBenchmarkData,'project_proposal_id': project_proposal_id})


class MonitorCreate(AjaxableResponseMixin,CreateView):
    """
    Monitor Form
    """
    model = Monitor

    def dispatch(self, request, *args, **kwargs):
        return super(MonitorCreate, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(MonitorCreate, self).get_context_data(**kwargs)
        context.update({'id': self.kwargs['id']})
        return context

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
        messages.success(self.request, 'Success, Monitor Created!')
        return self.render_to_response(self.get_context_data(form=form))

    form_class = MonitorForm


class MonitorUpdate(AjaxableResponseMixin, UpdateView):
    """
    Monitor Form
    """

    model = Monitor

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid Form', fail_silently=False)
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Success, Monitor Updated!')

        return self.render_to_response(self.get_context_data(form=form))

    form_class = MonitorForm


class MonitorDelete(AjaxableResponseMixin, DeleteView):
    """
    Monitor Form
    """
    model = Monitor
    success_url = reverse_lazy('monitor_list')

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):

        form.save()

        messages.success(self.request, 'Success, Monitor Deleted!')
        return self.render_to_response(self.get_context_data(form=form))

    form_class = MonitorForm


class BenchmarkCreate(AjaxableResponseMixin, CreateView):
    """
    Benchmark Form
    """
    model = Benchmarks

    def dispatch(self, request, *args, **kwargs):
        return super(BenchmarkCreate, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(BenchmarkCreate, self).get_context_data(**kwargs)
        context.update({'id': self.kwargs['id']})
        return context

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
        messages.success(self.request, 'Success, Benchmark Created!')
        return self.render_to_response(self.get_context_data(form=form))

    form_class = BenchmarkForm


class BenchmarkUpdate(AjaxableResponseMixin, UpdateView):
    """
    Benchmark Form
    """
    model = Benchmarks

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid Form', fail_silently=False)
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Success, Benchmark Updated!')

        return self.render_to_response(self.get_context_data(form=form))

    form_class = BenchmarkForm


class BenchmarkDelete(AjaxableResponseMixin, DeleteView):
    """
    Benchmark Form
    """
    model = Benchmarks
    success_url = reverse_lazy('benchmark_list')

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):

        form.save()

        messages.success(self.request, 'Success, Benchmark Deleted!')
        return self.render_to_response(self.get_context_data(form=form))

    form_class = BenchmarkForm


class TrainingList(ListView):
    """
    Training Attendance
    """
    model = TrainingAttendance
    template_name = 'activitydb/training_list.html'

    def get(self, request, *args, **kwargs):

        project_proposal_id = self.kwargs['pk']

        if int(self.kwargs['pk']) == 0:
            getTraining = TrainingAttendance.objects.all()
        else:
            getTraining = TrainingAttendance.objects.all().filter(project_proposal_id=self.kwargs['pk'])

        return render(request, self.template_name, {'getTraining': getTraining, 'project_proposal_id': project_proposal_id})


class TrainingCreate(CreateView):
    """
    Training Form
    """
    model = TrainingAttendance

    def dispatch(self, request, *args, **kwargs):
        return super(TrainingCreate, self).dispatch(request, *args, **kwargs)

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
        messages.success(self.request, 'Success, Training Created!')
        return self.render_to_response(self.get_context_data(form=form))

    form_class = TrainingAttendanceForm


class TrainingUpdate(UpdateView):
    """
    Training Form
    """
    model = TrainingAttendance

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid Form', fail_silently=False)
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Success, Training Updated!')

        return self.render_to_response(self.get_context_data(form=form))

    form_class = TrainingAttendanceForm


class TrainingDelete(DeleteView):
    """
    Training Delete
    """
    model = TrainingAttendance
    success_url = reverse_lazy('training_list')

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):

        form.save()

        messages.success(self.request, 'Success, Training Deleted!')
        return self.render_to_response(self.get_context_data(form=form))

    form_class = TrainingAttendanceForm


class BeneficiaryList(ListView):
    """
    Beneficiary
    """
    model = Beneficiary
    template_name = 'activitydb/beneficiary_list.html'

    def get(self, request, *args, **kwargs):

        project_proposal_id = self.kwargs['pk']

        if int(self.kwargs['pk']) == 0:
            getBeneficiaries = Beneficiary.objects.all()
        else:
            getBeneficiaries = Beneficiary.objects.all().filter(training_id=self.kwargs['pk'])

        return render(request, self.template_name, {'getBeneficiaries': getBeneficiaries, 'project_proposal_id': project_proposal_id})


class BeneficiaryCreate(CreateView):
    """
    Beneficiary Form
    """
    model = Beneficiary

    def dispatch(self, request, *args, **kwargs):
        return super(BeneficiaryCreate, self).dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = {
            'training': self.kwargs['id'],
            }

        return initial

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Success, Beneficiary Created!')
        return self.render_to_response(self.get_context_data(form=form))

    form_class = BeneficiaryForm


class BeneficiaryUpdate(UpdateView):
    """
    Training Form
    """
    model = Beneficiary

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid Form', fail_silently=False)
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Success, Beneficiary Updated!')

        return self.render_to_response(self.get_context_data(form=form))

    form_class = BeneficiaryForm


class BeneficiaryDelete(DeleteView):
    """
    Beneficiary Delete
    """
    model = Beneficiary
    success_url = reverse_lazy('training_list')

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):

        form.save()

        messages.success(self.request, 'Success, Beneficiary Deleted!')
        return self.render_to_response(self.get_context_data(form=form))

    form_class = BeneficiaryForm


class QuantitativeOutputsList(ListView):
    """
    QuantitativeOutput List
    """
    model = QuantitativeOutputs
    template_name = 'activitydb/quantitative_list.html'

    def get(self, request, *args, **kwargs):

        project_proposal_id = self.kwargs['pk']

        if int(self.kwargs['pk']) == 0:
            getQuantitativeOutputs = QuantitativeOutputs.objects.all()
        else:
            getQuantitativeOutputs = QuantitativeOutputs.objects.all().filter(project_proposal_id=self.kwargs['pk'])

        return render(request, self.template_name, {'getQuantitativeOutputs': getQuantitativeOutputs, 'project_proposal_id': project_proposal_id})


class QuantitativeOutputsCreate(AjaxableResponseMixin, CreateView):
    """
    QuantitativeOutput Form
    """
    model = QuantitativeOutputs

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


class QuantitativeOutputsUpdate(AjaxableResponseMixin, UpdateView):
    """
    QuantitativeOutput Form
    """
    model = QuantitativeOutputs

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


class QuantitativeOutputsDelete(AjaxableResponseMixin, DeleteView):
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


class BudgetList(ListView):
    """
    QuantitativeOutput List
    """
    model = Budget
    template_name = 'activitydb/budget_list.html'

    def get(self, request, *args, **kwargs):

        project_proposal_id = self.kwargs['pk']

        if int(self.kwargs['pk']) == 0:
            getBudget = Budget.objects.all()
        else:
            getBudget = Budget.objects.all().filter(project_proposal_id=self.kwargs['pk'])

        return render(request, self.template_name, {'getBudget': getBudget, 'project_proposal_id': project_proposal_id})


class BudgetCreate(AjaxableResponseMixin, CreateView):
    """
    QuantitativeOutput Form
    """
    model = Budget

    def get_context_data(self, **kwargs):
        context = super(BudgetCreate, self).get_context_data(**kwargs)
        context.update({'id': self.kwargs['id']})
        return context

    def dispatch(self, request, *args, **kwargs):
        return super(BudgetCreate, self).dispatch(request, *args, **kwargs)

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
        messages.success(self.request, 'Success, Budget Created!')
        form = ""
        return self.render_to_response(self.get_context_data(form=form))


    form_class = BudgetForm


class BudgetUpdate(AjaxableResponseMixin, UpdateView):
    """
    QuantitativeOutput Form
    """
    model = Budget

    def get_context_data(self, **kwargs):
        context = super(BudgetUpdate, self).get_context_data(**kwargs)
        context.update({'id': self.kwargs['pk']})
        return context

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid Form', fail_silently=False)
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Success, Quantitative Output Updated!')

        return self.render_to_response(self.get_context_data(form=form))

    form_class = BudgetForm


class BudgetDelete(AjaxableResponseMixin, DeleteView):
    """
    QuantitativeOutput Delete
    """
    model = Budget
    success_url = '/'

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):

        form.save()

        messages.success(self.request, 'Success, Quantitative Output Deleted!')
        return self.render_to_response(self.get_context_data(form=form))

    form_class = BudgetForm


def report(request):
    """
    Show LIST of submitted incidents with a filtered search view using django-tables2
    and django-filter
    """
    countries=getCountry(request.user)
    getAgreements = ProjectAgreement.objects.select_related().filter(program__country__in=countries)
    filtered = ProjectAgreementFilter(request.GET, queryset=getAgreements)
    table = ProjectAgreementTable(filtered.queryset)
    table.paginate(page=request.GET.get('page', 1), per_page=20)

    if request.method == "GET" and "search" in request.GET:
        #list1 = list()
        #for obj in filtered:
        #    list1.append(obj)
        """
         fields = ['country','activity_code', 'project_name', 'beneficiary_type', 'project_proposal', 'activity_code',
         'office', 'program', 'sector','approval_status', 'approved by', 'approved date'
        """
        queryset = ProjectAgreement.objects.filter(
                                           Q(activity_code__contains=request.GET["search"]) |
                                           Q(project_name__contains=request.GET["search"]) |
                                           Q(beneficiary_type__contains=request.GET["search"]) |
                                           Q(approval__contains=request.GET["search"]) |
                                           Q(office__name__contains=request.GET["search"]) |
                                           Q(sector__name__contains=request.GET["search"]) |
                                           Q(program__name__contains=request.GET["search"])).select_related()
        table = ProjectAgreementTable(queryset)

    RequestConfig(request).configure(table)

    # send the keys and vars from the json data to the template along with submitted feed info and silos for new form
    return render(request, "activitydb/report.html", {'get_agreements': table, 'country': countries, 'form': FilterForm(), 'filter': filtered, 'helper': FilterForm.helper})

def doImport(request, pk):
    """
    Copy the selected Silo data into the Project Proposal tables letting the user map
    the columns first
    :param request:
    :param pk:
    :return:
    """
    from_silo_id = pk

    getSourceFrom = DataField.objects.all().filter(silo__id=from_silo_id).values('name').distinct()
    getSourceTo = ProjectProposal._meta.get_all_field_names()
    users = User.objects.all()


    return render(request, "activitydb/merge-column-form.html", {'getSourceFrom':getSourceFrom, 'getSourceTo':getSourceTo, 'from_silo_id':from_silo_id, 'users':users})

def country_json(request, country):
    """
    For populating the province dropdown based  country dropdown value
    """
    selected_country = Country.objects.get(id=country)
    province = Province.objects.all().filter(country=selected_country)
    provinces_json = serializers.serialize("json", province)
    return HttpResponse(provinces_json, content_type="application/json")

def province_json(request, province):
    """
    For populating the office district based  country province value
    """
    selected_province = Province.objects.get(id=province)
    district = District.objects.all().filter(province=selected_province)
    districts_json = serializers.serialize("json", district)
    return HttpResponse(districts_json, content_type="application/json")

def district_json(request, district):
    """
    For populating the office dropdown based  country dropdown value
    """
    selected_district = District.objects.get(id=district)
    village = Village.objects.all().filter(district=selected_district)
    villages_json = serializers.serialize("json", village)
    return HttpResponse(villages_json, content_type="application/json")

def doMerge(request, pk):
    """
    Copy the selected Silo data into the Project Proposal tables letting the user map
    the columns first
    :param request:
    :return:
    """
    from_silo_id = pk
    approved_by = None
    approval_submitted_by = None

    # Empty dict
    fields_to_insert = {}
    fields_to_ignore = {}

    #more then one record might be returning so get the row_numbers as a count and loop over each
    get_rows = ValueStore.objects.values('row_number').filter(field__silo__id=from_silo_id).distinct()
    for row in get_rows:
        #now loop over each column in the post and check if a mapping was made
        #request.POST[column] = Form field value
        #column = Form field name(variable)
        for column in request.POST:
            try:
                getSourceFrom = ValueStore.objects.get(field__silo__id=from_silo_id, field__name=str(column), row_number=row['row_number'])
            except Exception as e:
                getSourceFrom = None


            if request.POST[column] != "Ignore" and request.POST[column] != "0" and str(column) != "csrfmiddlewaretoken" and str(column) != "from_column_id" and str(column) != "from_silo_id":
                fields_to_insert[str(request.POST[column])] = str(getSourceFrom.char_store)
            else:
                fields_to_ignore[str(request.POST[column])] = str(getSourceFrom.char_store)

        #set program ID and throw if not found
        try:
            programs, created = Program.objects.get_or_create(name__icontains=program_value)
            program_id = programs.pk
        except Exception as e:
            program_id = None
            messages.add_message(request, messages.INFO, "Program ID not found, a program is required for each new project proposal.")
        country = getCountry(request.user)
        country_id = country

        new_project_proposal = ProjectProposal.objects.create(approved_by=approved_by, approval_submitted_by=approval_submitted_by, **fields_to_insert)
        new_project_proposal.save()

    redirect_url = "/activitydb/projectproposal_update/" + str(new_project_proposal.id)

    return HttpResponseRedirect(redirect_url)



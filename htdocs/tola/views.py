from django.shortcuts import render
from .forms import FeedbackForm, RegistrationForm
from django.contrib import messages
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import auth
from activitydb.models import ProjectAgreement, ProjectProposal, ProjectComplete, Program, Community, Sector
from djangocosign.models import UserProfile
from djangocosign.models import Country
from activitydb.models import Country as ActivityCountry
from util import getCountry
from datetime import datetime
from django.shortcuts import get_object_or_404

from tola.util import getCountry

def index(request):
    """
    Home page
    get count of proposals and agreements approved and total for dashboard
    """
    program_id = 0
    countries = getCountry(request.user)
    getPrograms = Program.objects.all().filter(funding_status="Funded", country__in=countries)
    getSectors = Sector.objects.all()

    agreement_total_count = ProjectAgreement.objects.all().filter(program__country__in=countries).count()
    proposal_total_count = ProjectProposal.objects.all().filter(program__country__in=countries).count()
    complete_total_count = ProjectComplete.objects.all().filter(program__country__in=countries).count()
    agreement_approved_count = ProjectAgreement.objects.all().filter(approval='approved', program__country__in=countries).count()
    proposal_approved_count = ProjectProposal.objects.all().filter(approval='approved', program__country__in=countries).count()
    complete_approved_count = ProjectComplete.objects.all().filter(approval='approved', program__country__in=countries).count()
    agreement_wait_count = ProjectAgreement.objects.all().filter(approval='in progress', program__country__in=countries).count()
    proposal_wait_count = ProjectProposal.objects.all().filter(approval='in progress', program__country__in=countries).count()
    complete_wait_count = ProjectComplete.objects.all().filter(approval='in progress', program__country__in=countries).count()

    if int(program_id) == 0:
        getCommunity = Community.objects.all().filter(country__in=countries)
    else:
        getCommunity = Community.objects.all().filter(projectproposal__program__id=program_id)

    return render(request, "index.html", {'agreement_total_count':agreement_total_count, 'proposal_total_count':proposal_total_count,\
                                          'agreement_approved_count':agreement_approved_count,'proposal_approved_count':proposal_approved_count,\
                                          'complete_approved_count':complete_approved_count,'complete_total_count':complete_total_count,
                                          'complete_wait_count':complete_wait_count,'proposal_wait_count':proposal_wait_count,'agreement_wait_count':agreement_wait_count,
                                          'programs':getPrograms,'getCommunity':getCommunity,'country': countries, 'getSectors':getSectors
                                          })

def dashboard(request,id):
    """
    Home page
    get count of proposals and agreements approved and total for dashboard
    """
    program_id = id
    getFilteredName=Program.objects.get(id=program_id)
    getName = getFilteredName.name
    countries = getCountry(request.user)
    getPrograms = Program.objects.all().filter(funding_status="Funded", country__in=countries)
    getSectors = Sector.objects.all()


    if int(program_id) == 0:
        agreement_total_count = ProjectAgreement.objects.all().filter(program__country__in=countries).count()
        proposal_total_count = ProjectProposal.objects.all().filter(program__country__in=countries).count()
        complete_total_count = ProjectComplete.objects.all().filter(program__country__in=countries).count()
        agreement_approved_count = ProjectAgreement.objects.all().filter(approval='approved', program__country__in=countries).count()
        proposal_approved_count = ProjectProposal.objects.all().filter(approval='approved', program__country__in=countries).count()
        complete_approved_count = ProjectComplete.objects.all().filter(approval='approved', program__country__in=countries).count()
        agreement_wait_count = ProjectAgreement.objects.all().filter(approval='in progress', program__country__in=countries).count()
        proposal_wait_count = ProjectProposal.objects.all().filter(approval='in progress', program__country__in=countries).count()
        complete_wait_count = ProjectComplete.objects.all().filter(approval='in progress', program__country__in=countries).count()
        getCommunity = Community.objects.all().filter(country__in=countries)
    else:
        agreement_total_count = ProjectAgreement.objects.all().filter(program__id=program_id, program__country__in=countries).count()
        proposal_total_count = ProjectProposal.objects.all().filter(program__id=program_id, program__country__in=countries).count()
        complete_total_count = ProjectComplete.objects.all().filter(program__id=program_id, program__country__in=countries).count()
        agreement_approved_count = ProjectAgreement.objects.all().filter(program__id=program_id, approval='approved', program__country__in=countries).count()
        proposal_approved_count = ProjectProposal.objects.all().filter(program__id=program_id, approval='approved', program__country__in=countries).count()
        complete_approved_count = ProjectComplete.objects.all().filter(program__id=program_id, approval='approved', program__country__in=countries).count()
        agreement_wait_count = ProjectAgreement.objects.all().filter(program__id=program_id, approval='in progress', program__country__in=countries).count()
        proposal_wait_count = ProjectProposal.objects.all().filter(program__id=program_id, approval='in progress', program__country__in=countries).count()
        complete_wait_count = ProjectComplete.objects.all().filter(program__id=program_id, approval='in progress', program__country__in=countries).count()
        getCommunity = Community.objects.all().filter(projectproposal__program__id=program_id)

    return render(request, "index.html", {'agreement_total_count':agreement_total_count, 'proposal_total_count':proposal_total_count,\
                                          'agreement_approved_count':agreement_approved_count,'proposal_approved_count':proposal_approved_count,\
                                          'complete_approved_count':complete_approved_count,'complete_total_count':complete_total_count,
                                          'complete_wait_count':complete_wait_count,'proposal_wait_count':proposal_wait_count,'agreement_wait_count':agreement_wait_count,
                                          'programs':getPrograms,'getCommunity':getCommunity,'country': countries,'getFilteredName':getName,'getSectors':getSectors
                                          })

def contact(request):
    """
    Feedback form
    """
    form = FeedbackForm(initial={'submitter': request.user})

    if request.method == 'POST':
        form = FeedbackForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            form.save()
            messages.error(request, 'Thank you', fail_silently=False)
        else:
            messages.error(request, 'Invalid', fail_silently=False)
            print form.errors

    return render(request, "contact.html", {'form': form, 'helper': FeedbackForm.helper})


def faq(request):
    return render(request, 'faq.html')


def documentation(request):
    return render(request, 'documentation.html')


def register(request):
    """
    Register a new User profile using built in Django Users Model
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {
        'form': form,
    })


def profile(request):
    """
    Update a User profile using built in Django Users Model if the user is logged in
    otherwise redirect them to registration version
    """
    if request.user.is_authenticated():
        obj = get_object_or_404(UserProfile, user=request.user)
        form = RegistrationForm(request.POST or None, instance=obj,initial={'username': request.user})

        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.error(request, 'Your profile has been updated.', fail_silently=False)

        return render(request, "registration/profile.html", {
            'form': form, 'helper': RegistrationForm.helper
        })
    else:
        return HttpResponseRedirect("/accounts/register")


def logout_view(request):
    """
    Logout a user
    """
    logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect("/")


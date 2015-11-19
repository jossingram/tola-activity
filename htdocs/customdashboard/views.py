from django.shortcuts import render
from django.contrib import messages
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import auth
from activitydb.models import ProjectAgreement, ProjectComplete, Program, SiteProfile, Sector,Country as ActivityCountry, Feedback, FAQ, DocumentationApp

from djangocosign.models import UserProfile
from djangocosign.models import Country

from util import getCountry
from datetime import datetime
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from django.db.models import Q

from tola.util import getCountry

from django.contrib.auth.decorators import login_required


@login_required(login_url='/accounts/login/')

def DefaultCustomDashboard(request,id=0,sector=0):
    """
    # of agreements, approved, rejected, waiting, archived and total for dashboard
    """
    program_id = id
    countries = getCountry(request.user)

    getFilteredName=Program.objects.get(id=program_id)
    getProjects = ProjectAgreement.objects.all().filter(program__id=program_id, program__country__in=countries)

    getSiteProfile = SiteProfile.objects.all().filter(projectagreement__program__id=program_id, projectagreement__sector__id=sector)
    getProjectStatus = ProjectAgreement.objects.all().filter(program__id=program_id).values('approval').distinct()

    return render(request, "customdashboard/visual_dashboard.html", {'getSiteProfile':getSiteProfile,'country': countries,
                                                                     'getFilteredName':getFilteredName,'getProjects': getProjects})
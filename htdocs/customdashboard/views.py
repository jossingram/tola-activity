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
    getSectors = Sector.objects.all().exclude(program__isnull=True).select_related()

    if int(sector) == 0:
        getPrograms = Program.objects.all().filter(funding_status="Funded", country__in=countries).exclude(agreement__isnull=True)
        sectors = Sector.objects.all()
    else:
        getPrograms = Program.objects.all().filter(funding_status="Funded", country__in=countries, sector=sector).exclude(agreement__isnull=True)
        sectors = Sector.objects.all().filter(id=sector)

    if int(program_id) == 0:
        getFilteredName=None
        agreement_total_count = ProjectAgreement.objects.all().filter(sector__in=sectors, program__country__in=countries).count()
        complete_total_count = ProjectComplete.objects.all().filter(project_agreement__sector__in=sectors, program__country__in=countries).count()
        agreement_approved_count = ProjectAgreement.objects.all().filter(approval='approved', sector__in=sectors, program__country__in=countries).count()
        complete_approved_count = ProjectComplete.objects.all().filter(approval='approved', project_agreement__sector__in=sectors, program__country__in=countries).count()
        agreement_open_count = ProjectAgreement.objects.all().filter(approval='open', sector__id__in=sectors, program__country__in=countries).count()
        complete_open_count = ProjectComplete.objects.all().filter(Q(Q(approval='open') | Q(approval="")), project_agreement__sector__in=sectors, program__country__in=countries).count()
        agreement_wait_count = ProjectAgreement.objects.all().filter(approval='in progress', sector__in=sectors, program__country__in=countries).count()
        complete_wait_count = ProjectComplete.objects.all().filter(approval='in progress', project_agreement__sector__in=sectors, program__country__in=countries).count()
        if int(sector) > 0:
            getSiteProfile = SiteProfile.objects.all().filter(Q(Q(projectagreement__sector__in=sectors)), country__in=countries)
        else:
            getSiteProfile = SiteProfile.objects.all().filter(country__in=countries)


    else:
        getFilteredName=Program.objects.get(id=program_id)
        agreement_total_count = ProjectAgreement.objects.all().filter(program__id=program_id, program__country__in=countries).count()
        complete_total_count = ProjectComplete.objects.all().filter(program__id=program_id, program__country__in=countries).count()
        agreement_approved_count = ProjectAgreement.objects.all().filter(program__id=program_id, approval='approved', program__country__in=countries).count()
        complete_approved_count = ProjectComplete.objects.all().filter(program__id=program_id, approval='approved', program__country__in=countries).count()
        agreement_open_count = ProjectAgreement.objects.all().filter(program__id=program_id, approval='open', program__country__in=countries).count()
        complete_open_count = ProjectComplete.objects.all().filter(Q(Q(approval='open') | Q(approval="")), program__id=program_id, program__country__in=countries).count()
        agreement_wait_count = ProjectAgreement.objects.all().filter(program__id=program_id, approval='in progress', program__country__in=countries).count()
        complete_wait_count = ProjectComplete.objects.all().filter(program__id=program_id, approval='in progress', program__country__in=countries).count()
        getSiteProfile = SiteProfile.objects.all().filter(projectagreement__program__id=program_id, projectagreement__sector__id=sector)




    return render(request, "customdashboard/visual_dashboard.html", {'agreement_total_count':agreement_total_count,\
                                          'agreement_approved_count':agreement_approved_count,\
                                          'agreement_open_count':agreement_open_count,\
                                          'agreement_wait_count':agreement_wait_count,\
                                          'complete_open_count':complete_open_count,\
                                          'complete_approved_count':complete_approved_count,'complete_total_count':complete_total_count,\
                                          'complete_wait_count':complete_wait_count,\
                                          'programs':getPrograms,'getSiteProfile':getSiteProfile,'country': countries,'getFilteredName':getFilteredName,'getSectors':getSectors,\
                                          'sector': sector
                                          })
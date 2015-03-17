from django.shortcuts import render
from .forms import FeedbackForm, RegistrationForm
from django.contrib import messages
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import auth
from activitydb.models import ProjectAgreement, ProjectProposal


def index(request):
    """
    Home page
    get count of proposals and agreemtns approved and total for progress gauges
    """
    agreement_total_count = ProjectAgreement.objects.all().count()
    proposal_total_count = ProjectProposal.objects.all().count()
    agreement_approved_count = ProjectAgreement.objects.all().filter(approval='approved').count()
    proposal_approved_count = ProjectProposal.objects.all().filter(approval='approved').count()

    return render(request, "index.html", {'agreement_total_count':agreement_total_count, 'proposal_total_count':proposal_total_count,'agreement_approved_count':agreement_approved_count,'proposal_approved_count':proposal_approved_count })

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
        temp_post = request.POST.copy()
        temp_post['last_login'] = request.user.last_login
        temp_post['is_active'] = request.user.is_active
        temp_post['is_superuser'] = request.user.is_superuser
        temp_post['last_login'] = request.user.last_login
        temp_post['is_staff'] = request.user.is_staff
        temp_post['date_joined'] = request.user.date_joined

        if request.method == 'POST':
            form = RegistrationForm(temp_post, instance=request.user)

            if form.is_valid():
                form.save()
                messages.error(request, 'Your profile has been updated.', fail_silently=False)
            else:
                messages.error(request, 'Invalid', fail_silently=False)
                print form.errors
        else:
            form = RegistrationForm(instance=request.user)
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


from django.conf import settings
from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.utils.http import is_safe_url, urlsafe_base64_decode
from django.shortcuts import resolve_url
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .forms import HunterCreationForm
from .models import Hunter, Hunt, Watch
from .logic import topHunters, activeHunts
from .mammoth.forms import MammothForm
from .message.forms import MessageForm
from .hunt.forms import HuntSubmit


@login_required
def index(request):
    if not request.user.is_authenticated:
        return redirect('accounts/login')

    context = {}

    topHunters(context)
    activeHunts(context)

    watches = Watch.objects.filter(hunters=request.user.id)
    # find out if hunter is active watch
    for watch in watches:
        if watch.active:
            context['onwatch'] = True
            context['mammothform'] = MammothForm()
            context['messageform'] = MessageForm()
            break
    else:
        # no active watch found
        hunts = Hunt.objects.filter(hunters=request.user.id)
        # find out if hunter is in unfinished hunt
        for hunt in hunts:
            if not hunt.finished:
                context['onhunt'] = True
                context['hunt'] = hunt
                context['huntform'] = HuntSubmit(instance=hunt)
                break


    return render(request, 'app/index.html', context)
"""
def gentella_html(request):
    if not request.user.is_authenticated:
        return requireLogin(request)

    context = {}
    # The template to be loaded as per hunters.
    # All resource paths for hunters end in .html.

    # Pick out the html file name from the url. And load that template.
    load_template = request.path.split('/')[-1]
    template = 'app/' + load_template
    return render(request, template, context)
"""

def register(request):

    context = {'form': HunterCreationForm}

    if request.method == 'POST':
        # user creation
        form = HunterCreationForm(request.POST)
        if form.is_valid():
            hunter = form.save(commit=False)

            # assign hunter role to hunter
            hunter.role = 0

            # save user to DB
            hunter.save()

            # now you can log in
            return redirect('/')
        else:
            context['error'] = 'Invalid username or password'

    return render(request, 'registration/register.html', context)


def setManagerPermissions(user):
    pass

def setOfficerPermissions(user):
    pass


@sensitive_post_parameters()
@csrf_protect
@never_cache
def login(request):
    """
    Displays the login form and handles the login action.
    """
    redirect_field = REDIRECT_FIELD_NAME
    authentication_form = AuthenticationForm

    redirect_to = request.POST.get(redirect_field, request.GET.get(redirect_field, ''))

    if request.method == "POST":
        form = authentication_form(request, data=request.POST)
        if form.is_valid():

            # Ensure the user-originating redirection url is safe.
            if not is_safe_url(url=redirect_to, host=request.get_host()):
                redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

            user = form.get_user()
            # Okay, security check complete. Log the user in.
            auth_login(request, user)

            hunter = Hunter.objects.get(pk=user.id)

            if hunter.role == 'Officer':
                setOfficerPermissions(user)
            elif hunter.role == 'Manager':
                setManagerPermissions(user)

            return redirect(redirect_to)
    else:
        form = authentication_form(request)

    current_site = get_current_site(request)

    context = {
        'form': form,
        redirect_field: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
    }

    return render(request, 'registration/login.html', context)

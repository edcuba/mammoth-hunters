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
from django.contrib import messages


@login_required
def index(request):
    if not request.user.is_authenticated:
        return redirect('accounts/login')

    context = {}

    topHunters(context)
    activeHunts(context)

    watch = Watch.objects.filter(hunters=request.user.id, active=True).first()

    if watch:
        context['onwatch'] = True
        context['mammothform'] = MammothForm()
        context['messageform'] = MessageForm()
    else:
        # no active watch found
        hunt = Hunt.objects.filter(hunters=request.user.id, finished=False).first()
        if hunt:
            context['onhunt'] = True
            context['hunt'] = hunt
            context['huntform'] = HuntSubmit(instance=hunt)

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

    context = {}
    form  = HunterCreationForm()

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
            messages.success(request, "Registration successful")
            return redirect('login')
        else:
            messages.error(request, "Registration failed")

    context['form'] = form
    return render(request, 'registration/register.html', context)


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

            return redirect(redirect_to)

        messages.error(request, "Login failed")

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

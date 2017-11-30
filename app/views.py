from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .forms import HunterCreationForm
from .models import Hunter, Hunt
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


    # hunter is on watch
    context['onwatch'] = True
    context['mammothform'] = MammothForm()
    context['messageform'] = MessageForm()

    # TODO hunter is on hunt
    hunt = Hunt.objects.get(pk=1)
    context['onhunt'] = True
    context['hunt'] = hunt
    submitForm = HuntSubmit(instance=hunt)
    context['huntform'] = submitForm


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

            # add hunter to Hunters group
            g = Group.objects.get(name='Hunters')
            hunter.groups.add(g)

            # now you can log in
            return redirect('/')
        else:
            context['error'] = 'Invalid username or password'

    return render(request, 'registration/register.html', context)

from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    if not request.user.is_authenticated:
        return redirect('accounts/login')

    context = {}
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

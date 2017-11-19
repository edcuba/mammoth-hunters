from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from .. import views as appView
from ..models import Hunter

def requireLogin(request):
    """ Render login screen or process login """
    form = None
    error = None
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = Hunter.objects.get(username=username)
            if user is not None:
                login(request, user)
                return appView.index(request)
        form.password = None
        error = "Login failed"

    context = {'loginForm': form or LoginForm(), 'error': error}
    return render(request, 'app/login.html', context)

from django.shortcuts import render, redirect
from ..models import Hunt
from .forms import HuntDetails, HuntForm, HuntSubmit
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from ..security import privileged_check


@login_required
def huntList(request):
    context = {}
    hunts = Hunt.objects.all().order_by('finished', '-id')
    context['hunts'] = hunts
    for hunt in context['hunts']:
        try:
            if hunt.target.killedIn.id == hunt.id:
                hunt.successful = 'Yes'
        except:
            hunt.successful = 'No'

    return render(request, 'app/hunt/list.html', context)

@login_required
@user_passes_test(privileged_check)
def detail(request):
    context = {}

    if request.method == 'POST':
        hunt = Hunt.objects.get(pk=request.session['id_hunt'])
        form = HuntDetails(request.POST, instance=hunt)
        if form.is_valid():
            hunt = form.save()
            for hunter in hunt.hunters.all():
                hunter.killedIn = None
                hunter.save()
            died = form.cleaned_data.get('deadHunters', [])
            for hunter in died:
                hunter.killedIn = hunt
                hunter.save()
            return redirect('hunt_list')
    else:
        huntID = request.GET.get('id_hunt')
        request.session['id_hunt'] = huntID
        try:
            hunt = Hunt.objects.get(pk=huntID)
            context['form'] = HuntDetails(instance=hunt)
        except:
            return redirect('hunt_list')

    context['action'] = reverse("hunt_detail")

    return render(request, 'app/hunt/detail.html', context)

def formError(request, context, msg="Form invalid"):
    context['error'] = "Error: " + msg
    return render(request, context['action'], context)


@login_required
@user_passes_test(privileged_check)
def add(request):
    context = {}
    context['action'] = reverse("hunt_add")

    if request.method == 'POST':
        form = HuntForm(request.POST)

        context['form'] = form

        if form.is_valid():
            hunt = form.save()
            return redirect("hunt_list")

        return formError(request, context)

    context['form'] = HuntForm()

    return render(request, 'app/hunt/detail.html', context)

@login_required
def submit(request):
    if request.method != 'POST':
        return redirect('index')

    hunts = Hunt.objects.filter(hunters=request.user.id)
    form = None
    # find out if hunter is in unfinished hunt
    for hunt in hunts:
        if not hunt.finished:
            form = HuntSubmit(request.POST, instance=hunt)
            break

    if not form or not form.is_valid():
        return redirect('index')

    hunt = form.save()
    killed = form.cleaned_data.get('mammothKilled')

    if killed:
        target = hunt.target
        target.killedIn = hunt
        target.health = 0
        target.save()

    died = form.cleaned_data.get('deadHunters', [])
    for hunter in died:
        hunter.killedIn = hunt
        hunter.save()

    hunt.finished = True
    hunt.save()

    return redirect('index')

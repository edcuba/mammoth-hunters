from django.shortcuts import render, redirect
from ..models import Hunt, Hunter
from .forms import HuntDetails, HuntForm, HuntSubmit
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from ..security import manager_check, privileged_check
from django.contrib import messages


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
#@user_passes_test(privileged_check)
def detail(request):
    context = {}

    if request.method == 'POST':
        hunt = Hunt.objects.get(pk=request.session['id_hunt'])
        form = HuntDetails(request.POST, instance=hunt)
        # TODO zabit mamuta, nastavit mamutovy health na 0
        # pri obnoveni na 1 (Ako u huntera)
        if form.is_valid():
            hunt = form.save()
            for hunter in hunt.hunters.all():
                hunter.killedIn = None
                hunter.health = 1
                hunter.save()
            died = form.cleaned_data.get('deadHunters', [])
            for hunter in died:
                hunter.killedIn = hunt
                hunter.health = 0
                hunter.save()
            messages.success(request, "Hunt updated")
            return redirect('hunt_list')
        messages.error(request, "Hunt update failed")
    else:
        huntID = request.GET.get('id_hunt')
        request.session['id_hunt'] = huntID
        try:
            hunt = Hunt.objects.get(pk=huntID)
            context['form'] = HuntDetails(instance=hunt)
            context['hunt'] = hunt
            hunt.died = Hunter.objects.filter(killedIn=hunt.id)
            try:
                if hunt.target.killedIn.id == hunt.id:
                    hunt.successful = 'Yes'
            except:
                hunt.successful = 'No'
        except:
            return redirect('hunt_list')
    
    context['action'] = reverse("hunt_detail")

    return render(request, 'app/hunt/detail.html', context)

@login_required
@user_passes_test(manager_check)
def add(request):
    context = {}
    context['action'] = reverse("hunt_add")

    if request.method == 'POST':
        form = HuntForm(request.POST)

        context['form'] = form

        if form.is_valid():
            hunt = form.save()
            messages.success(request, "Hunt created")
            return redirect("hunt_list")

        messages.error(request, "Hunt creation failed")
        return render(request, context['action'], context)

    context['form'] = HuntForm()

    return render(request, 'app/hunt/detail.html', context)


@login_required
def submit(request):
    if request.method != 'POST':
        return redirect('index')

    hunt = Hunt.objects.filter(hunters=request.user.id, finished=False).first()
    if not hunt:
        messages.error(request, "No active hunt")
        return redirect('index')

    form = HuntSubmit(request.POST, instance=hunt)

    if not form or not form.is_valid():
        messages.error(request, "Hunt form invalid")
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

    messages.success(request, "Hunt report submitted")
    return redirect('index')

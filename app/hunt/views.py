from django.shortcuts import render, redirect
from ..models import Hunt
from .forms import HuntDetails, HuntForm


def huntList(request):
    context = {}
    hunts = Hunt.objects.all()
    context['hunts'] = hunts

    return render(request, 'app/hunt/list.html', context)

def detail(request):
    context = {}
    huntID = request.GET.get('id_hunt')

    try:
        hunt = Hunt.objects.get(pk=huntID)
        context['form'] = HuntDetails(instance=hunt)
    except:
        context['form'] = HuntForm()

    return render(request, 'app/hunt/detail.html', context)

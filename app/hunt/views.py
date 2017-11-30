from django.shortcuts import render, redirect
from ..models import Hunt
from .forms import HuntDetails


def huntList(request):
    context = {}
    hunts = Hunt.objects.all()
    context['hunts'] = hunts

    return render(request, 'app/hunt/list.html', context)

def detail(request):
    context = {}
    huntID = request.GET.get('id_hunt')
    if not huntID:
        return redirect('index')

    try:
        hunt = Hunt.objects.get(pk=huntID)
    except:
        return redirect('index')

    context['form'] = HuntDetails(instance=hunt)
    return render(request, 'app/hunt/detail.html', context)

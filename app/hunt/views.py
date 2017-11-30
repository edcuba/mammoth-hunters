from django.shortcuts import render
from ..models import Hunt


def huntList(request):
    context = {}
    hunts = Hunt.objects.all()
    context['hunts'] = hunts

    return render(request, 'app/hunt/list.html', context)

def detail(request):
    context = {}

    return render(request, 'app/hunt/detail.html', context)

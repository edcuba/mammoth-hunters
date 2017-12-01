from django.shortcuts import render
from ..models import Pit
from .forms import PitForm

def pitList(request):
    context = {}

    pits = Pit.objects.all()

    context['pits'] = pits
    context['form'] = PitForm()

    return render(request, 'app/pit/list.html', context)

def add(request):
    pass
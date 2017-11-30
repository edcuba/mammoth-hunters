from django.shortcuts import render
from ..models import Pit

def pitList(request):
    context = {}

    pits = Pit.objects.all()

    context['pits'] = pits

    return render(request, 'app/pit/list.html', context)

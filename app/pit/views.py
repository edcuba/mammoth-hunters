from django.shortcuts import render
from ..models import Pit
from .forms import PitForm
from django.contrib.auth.decorators import login_required


@login_required
def pitList(request):
    context = {}

    context['form'] = PitForm()
    if request.method == 'POST':
        context['form'] = PitForm(request.POST)
        if context['form'].is_valid():
            context['form'].save()
    pits = Pit.objects.all()
    context['pits'] = pits
    return render(request, 'app/pit/list.html', context)

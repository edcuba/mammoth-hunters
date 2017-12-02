from django.shortcuts import render
from ..models import Pit
from .forms import PitForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages



@login_required
def pitList(request):
    context = {}

    context['form'] = PitForm()

    if request.method == 'POST':
        context['form'] = PitForm(request.POST)
        if context['form'].is_valid():
            context['form'].save()
            messages.success(request, "Pit created")
        else:
            messages.error(request, "Pit wasn't created")
    pits = Pit.objects.all().order_by('-id')

    context['pits'] = pits
    return render(request, 'app/pit/list.html', context)

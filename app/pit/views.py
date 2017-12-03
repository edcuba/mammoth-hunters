from django.shortcuts import render, redirect
from ..models import Pit, Hunt
from .forms import PitForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from ..security import manager_check



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
    for pit in pits:
        hunt = Hunt.objects.filter(pit=pit.id, finished=False).first()
        pit.hunt = hunt

    context['pits'] = pits
    return render(request, 'app/pit/list.html', context)

@login_required
def detail(request):
    cont = {}
    pit_id = request.GET.get('id_pit')
    pit = Pit.objects.get(pk=pit_id)
    hunt = Hunt.objects.filter(pit=pit.id, finished=False).first()
    pit.hunt = hunt
    cont['pit'] = pit
    return render(request, 'app/pit/detail.html', cont)

@login_required
@user_passes_test(manager_check)
def lock(request):
    cont = {}
    pit_id = request.GET.get('id_pit')
    pit = Pit.objects.get(pk=pit_id)
    pit.taken = not pit.taken
    pit.save()
    return redirect('pit_list')
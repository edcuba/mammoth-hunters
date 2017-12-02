from django.shortcuts import render
from ..models import Pit, Hunt
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
    pits = Pit.objects.all().order_by('-id')

    context['pits'] = pits
    return render(request, 'app/pit/list.html', context)

@login_required
def detail(request):
    cont = {}
    pit_id = request.GET.get('id_pit')
    pit = Pit.objects.get(pk=pit_id)
    hunt = Hunt.objects.filter(pit=pit.id)
    pit.hunt = hunt
    cont['pit'] = pit
    return render(request, 'app/pit/detail.html', cont)

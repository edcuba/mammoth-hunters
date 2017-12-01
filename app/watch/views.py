from django.shortcuts import render
from ..models import Watch
from .forms import WatchForm


def watchList(request):
    context = {}

    watches = Watch.objects.all()

    context['watches'] = watches
    return render(request, 'app/watch/list.html', context)

def detail(request):
    context = {}

    watchID = request.GET.get('id_watch')

    try:
        watch = Watch.objects.get(pk=watchID)
    except:
        watch = Watch()


    context['form'] = WatchForm(instance=watch)
    return render(request, 'app/watch/detail.html', context)

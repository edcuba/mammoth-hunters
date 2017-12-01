from django.shortcuts import render, redirect
from ..models import Watch
from .forms import WatchForm


def watchList(request):
    context = {}

    watches = Watch.objects.all().order_by('-active', '-id')

    context['watches'] = watches
    return render(request, 'app/watch/list.html', context)

def detail(request):
    context = {}

    if request.method == 'POST':
        form = WatchForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('watch_list')

    watchID = request.GET.get('id_watch')

    try:
        watch = Watch.objects.get(pk=watchID)
    except:
        watch = Watch()


    context['form'] = WatchForm(instance=watch)
    return render(request, 'app/watch/detail.html', context)


def end(request):

    watchid = request.GET.get('id_watch')
    try:
        watch = Watch.objects.get(pk=watchid)
        watch.active = False
        watch.save()
    except:
        pass
    return redirect('watch_list')

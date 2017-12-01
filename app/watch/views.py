from django.shortcuts import render, redirect
from ..models import Watch
from .forms import WatchForm
from django.contrib.auth.decorators import login_required, user_passes_test
from ..security import privileged_check


@login_required
def watchList(request):
    context = {}

    watches = Watch.objects.all().order_by('-active')

    context['watches'] = watches
    return render(request, 'app/watch/list.html', context)


@login_required
@user_passes_test(privileged_check)
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


@login_required
@user_passes_test(privileged_check)
def end(request):

    watchid = request.GET.get('id_watch')
    try:
        watch = Watch.objects.get(pk=watchid)
        watch.active = False
        watch.save()
    except:
        pass
    return redirect('watch_list')

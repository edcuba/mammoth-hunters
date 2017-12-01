from django.shortcuts import render, redirect
from .forms import MessageForm
from ..models import Watch


def messageList(request):
    return render(request, 'app/message/list.html')

def detail(request):
    return render(request, 'app/message/list.html')

def create(request):
    if request.method != 'POST':
        return redirect('index')

    form = MessageForm(request.POST)
    if not form.is_valid():
        return redirect('index')

    message = form.save(commit=False)

    activeWatch = None
    watches = Watch.objects.filter(hunters=request.user.id)
    # find out if hunter is active watch
    for watch in watches:
        if watch.active:
            activeWatch = watch
            break

    if not activeWatch:
        return redirect('index')

    message.from_watch = activeWatch
    message.save()

    activeWatch.active = False
    activeWatch.save()
    return redirect('index')

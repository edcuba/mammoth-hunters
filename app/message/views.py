from django.shortcuts import render, redirect
from .forms import MessageForm
from ..models import Watch
from django.contrib.auth.decorators import login_required, user_passes_test
from ..security import privileged_check

@login_required
@user_passes_test(privileged_check)
def messageList(request):
    return render(request, 'app/message/list.html')

@login_required
@user_passes_test(privileged_check)
def detail(request):
    return render(request, 'app/message/list.html')

@login_required
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

    return redirect('index')

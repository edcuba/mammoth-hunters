from django.shortcuts import render, redirect
from .forms import MessageForm
from ..models import Watch, Hunter, Message, Mammoth
from django.contrib.auth.decorators import login_required, user_passes_test
from ..security import privileged_check

@login_required
@user_passes_test(privileged_check)
def messageList(request):
    cont = {}
    hunter = Hunter.objects.get(pk=request.user.id)
    active_watch = Watch.objects.filter(hunters=hunter, active=True)
    if active_watch:
        cont['onwatch'] = True
    else:
        cont['onwatch'] = False

    cont['messages'] = Message.objects.all().order_by('-id')
    return render(request, 'app/message/list.html', cont)

@login_required
@user_passes_test(privileged_check)
def detail(request):
    cont = {}
    message_id = request.GET.get('id_message')
    message = Message.objects.get(pk=message_id)
    mammoths = Mammoth.objects.filter(message__in=message_id)
    message.watch_id = message.from_watch.id
    cont['message'] = message
    cont['mammoths'] = mammoths
    print("detail")
    return render(request, 'app/message/create.html', cont)

@login_required
def create(request):
    if request.method != 'POST':
        return redirect('index')

    form = MessageForm(request.POST)
    if not form.is_valid():
        return redirect('index')

    message = form.save(commit=False)

    activeWatch = None
    watch = Watch.objects.filter(hunters=request.user.id, active=True).first()

    # find out if hunter is active watch
    if watch:
        activeWatch = watch
    else:
        return redirect('index')

    message.from_watch = activeWatch
    message.save()
    message.mammoths = form.cleaned_data['mammoths']
    message.save()

    return redirect('index')

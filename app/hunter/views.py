from django.shortcuts import render
from ..models import Hunter

def profile(request):
    c = {}

    if request.method == 'POST':
        print(request.POST['id_hunter'])
        hunter = Hunter.objects.get(pk=request.POST['id_hunter'])
        c['hunter'] = hunter

    return render(request, 'app/hunter/profile.html', c)

def hunterList(request):
    context = {}
    context['hunters'] = Hunter.objects.all()
    return render(request, 'app/hunter/list.html', context)

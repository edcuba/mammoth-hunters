from django.shortcuts import render
from ..models import Hunter, ROLES, HunterAbilities

def profile(request):
    c = {}
    tmp = request.GET.get('id_hunter', request.user.id)
    hunter = Hunter.objects.get(pk=tmp)
    """
    if request.method == 'GET':
        print(request.POST['id_hunter'])
        hunter = Hunter.objects.get(pk=request.POST['id_hunter'])
    else:
        hunter = Hunter.objects.get(pk=request.user.id)
"""
    skills = HunterAbilities.objects.filter(hunter=hunter.id)
    c['role_name'] = ROLES[hunter.role][1]
    c['hunter'] = hunter
    return render(request, 'app/hunter/profile.html', c)

def hunterList(request):
    context = {}
    context['hunters'] = Hunter.objects.all()
    return render(request, 'app/hunter/list.html', context)

from django.shortcuts import render
from ..models import Hunter, ROLES, HunterAbilities, Watch, Hunt
from ..forms import HunterChangeForm

def profile(request):
    cont = {}
    tmp = request.GET.get('id_hunter', request.user.id)
    hunter = Hunter.objects.get(pk=tmp)
    hunter.role_name = ROLES[hunter.role][1]
    location = False
    act = ''
    try:
        location = Watch.objects.get(hunters=hunter.id, active=True).location
        act = 'Watching'
    except:
        pass
    try:
        location = Hunt.objects.get(hunter=hunter.id, finished=False).started_by.location
        act = 'Hunting'
    except:
        pass

    if not location:
        location = 'Cave'
    else:
        location = '{0} ({1})'.format(location, act)
    hunter.location = location

    if hunter.killedBy:
        hunter.alive = 'Dead'
    else:
        hunter.alive = 'Alive'
    cont['hunter'] = hunter
    try:
        cont['us'] = Hunter.objects.get(pk=request.user.id).role
    except:
        cont['us'] = 2
    
    cont['form'] = HunterChangeForm(instance=hunter)
    if cont['us'] != 2:
        for field in cont['form'].fields.values():
            field.widget.attrs['readonly'] = True
    if request.method == 'POST':
        cont['form'] = HunterChangeForm(request.POST, instance=hunter)
        if cont['form'].is_valid():
            hunter = cont['form'].save()
    

    cont['hunts'] = Hunt.objects.filter(hunters=hunter.id)

    return render(request, 'app/hunter/profile.html', cont)

def hunterList(request):
    cont = {}
    cont['hunters'] = Hunter.objects.all()
    for hunter in cont['hunters']:
        location = False
        act = ''
        try:
            location = Watch.objects.get(hunters=hunter.id, active=True).location
            act = 'Watching'
        except:
            pass
        try:
            location = Hunt.objects.get(hunter=hunter.id, finished=False).started_by.location
            watch = False
            act = 'Hunting'
        except:
            pass
        if not location:
            location = 'Cave'
        else:
            location = '{0} ({1})'.format(location, act)
        hunter.location = location
        hunter.role_name = ROLES[hunter.role][1]
        if hunter.killedBy:
            hunter.alive = 'Dead'
        else:
            hunter.alive = 'Alive'
        hunter.score = round((hunter.Strength +
                              hunter.Stamina +
                              hunter.Agility +
                              hunter.Intellect +
                              hunter.Speed)/100, 1)
    cont['stars'] = list(range(1, 6))
    return render(request, 'app/hunter/list.html', cont)

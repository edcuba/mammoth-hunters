from django.shortcuts import render
from ..models import Hunter, ROLES, HunterAbilities, Watch, Hunt
from ..forms import HunterChangeForm
from django.db.models import Count

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
        location = Hunt.objects.get(hunters=hunter.id, finished=False).pit.location
        act = 'Hunting'
    except:
        pass

    if not location:
        location = 'Cave'
    else:
        location = '{0} ({1})'.format(location, act)
    hunter.location = location

    if hunter.killedIn:
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
    for hunt in cont['hunts']:
        hunt.location = hunt.pit.location

    cont['watches'] = Watch.objects.filter(hunters=hunter.id)
    for watch in cont['watches']:
        watch.location = watch.location

    return render(request, 'app/hunter/profile.html', cont)

def hunterList(request):
    cont = {}
    cont['hunters'] = Hunter.objects.all().order_by('killedIn', 'first_name')
    for hunter in cont['hunters']:
        location = False
        act = ''
        try:
            location = Watch.objects.get(hunters=hunter.id, active=True).location
            act = 'Watching'
        except:
            pass
        try:
            location = Hunt.objects.get(hunters=hunter.id, finished=False).pit.location
            act = 'Hunting'
        except:
            pass
        if not location:
            location = 'Cave'
        else:
            location = '{0} ({1})'.format(location, act)
        hunter.location = location
        hunter.role_name = ROLES[hunter.role][1]
        if hunter.killedIn:
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

from django.shortcuts import render, redirect
from ..models import Hunter, ROLES, Watch, Hunt
from ..forms import HunterChangeForm
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from .forms import PasswdForm


@login_required
def profile(request):
    cont = {}

    cont['passwordform'] = PasswdForm(request.user)

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

    if hunter.killedIn or hunter.health <=0:
        hunter.alive = 'Dead'
    else:
        hunter.alive = 'Alive'
    cont['hunter'] = hunter

    cont['form'] = HunterChangeForm(instance=hunter)
    if not request.user.isOfficer():
        for field in cont['form'].fields.values():
            field.widget.attrs['readonly'] = True
    if request.method == 'POST':
        cont['form'] = HunterChangeForm(request.POST, instance=hunter)
        if cont['form'].is_valid():
            hunter = cont['form'].save()


    cont['hunts'] = Hunt.objects.filter(hunters=hunter.id).order_by('finished', '-id')
    for hunt in cont['hunts']:
        try:
            if hunt.target.killedIn.id == hunt.id:
                hunt.successful = 'Yes'
        except:
            hunt.successful = 'No'

    cont['watches'] = Watch.objects.filter(hunters=hunter.id).order_by('-active', '-id')

    return render(request, 'app/hunter/profile.html', cont)


@login_required
def hunterList(request):
    cont = {}
    cont['hunters'] = Hunter.objects.all()
    cont['hunters'] = cont['hunters'].extra(select={'living':"health > '0'"})
    cont['hunters'] = cont['hunters'].extra(order_by=['-living', 'first_name'])
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
        #last_hunt = Hunt.objects.filter(killedIn)
        if hunter.killedIn or hunter.health <= 0:
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


@login_required
def changePass(request):
    form = PasswdForm(request.user, request.POST)
    if form.is_valid():
        user = form.save()
        update_session_auth_hash(request, user)
        messages.success(request, 'Password updated')
    else:
        messages.error(request, 'Password update failed!')
    return redirect('hunter_profile')

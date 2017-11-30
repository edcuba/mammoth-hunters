from ..models import Mammoth, Message, Hunt
from django.shortcuts import render, redirect

def profile(request):
    cont = {}
    tmp = request.GET.get('id_mammoth')
    mammoth = Mammoth.objects.get(pk=tmp)
    location = False
    try:
        tmp_loc = Message.objects.filter(mammoths=mammoth.id).latest('id')
        location = tmp_loc.from_watch.location
    except:
        pass
    try:
        tmp_loc = Hunt.objects.filter(target=mammoth.id).latest('id')
        location = tmp_loc.pit.location
    except:
        pass
    
    if not location:
        location = 'Unknown'
    mammoth.location = location 
    if mammoth.hunted:
        mammoth.hunted = 'Yes'
    else:
        mammoth.hunted = 'No'
    if not mammoth.killedIn:
        mammoth.status = 'Alive'
    else:
        mammoth.status = 'Dead'
    cont['mammoth'] = mammoth

    cont['hunts'] = Hunt.objects.filter(target=mammoth.id)
    for hunt in cont['hunts']:
        hunt.location = hunt.pit.location
    return render(request, 'app/mammoth/profile.html', cont)

def mammothList(request):
    cont = {}

    cont['mammoths'] = Mammoth.objects.all()
    
    for mammoth in cont['mammoths']:
        try:
            tmp_loc = Message.objects.filter(mammoths=mammoth.id).latest('id')
            location = tmp_loc.from_watch.location
        except:
            location = 'Unknown'
        mammoth.location = location 
        if mammoth.hunted:
            mammoth.hunted = 'Yes'
        else:
            mammoth.hunted = 'No'
        
        if not mammoth.killedIn:
            mammoth.status = 'Alive'
        else:
            mammoth.status = 'Dead'
        
    return render(request, 'app/mammoth/list.html', cont)

def create(request):
    if request.method == 'POST':
        return redirect(request.POST['next'])
    return render(request, 'app/mammoth/profile.html')

from django.shortcuts import render

def profile(request):
    return render(request, 'app/hunter/profile.html')

def hunterList(request):
    return render(request, 'app/hunter/list.html')

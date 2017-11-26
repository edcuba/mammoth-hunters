from django.shortcuts import render

def profile(request):
    return render(request, 'app/mammoth/profile.html')

def mammothList(request):
    return render(request, 'app/mammoth/list.html')

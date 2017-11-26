from django.shortcuts import render

def huntList(request):
    return render(request, 'app/hunt/list.html')

def detail(request):
    return render(request, 'app/hunt/detail.html')

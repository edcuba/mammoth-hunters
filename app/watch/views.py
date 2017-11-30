from django.shortcuts import render


def detail(request):
    return render(request, 'app/watch/detail.html')

def watchList(request):
    return render(request, 'app/watch/list.html')

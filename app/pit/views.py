from django.shortcuts import render

def pitList(request):
    return render(request, 'app/pit/list.html')

from django.shortcuts import render

def messageList(request):
    return render(request, 'app/message/list.html')

def detail(request):
    return render(request, 'app/message/list.html')

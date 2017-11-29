from django.shortcuts import render, redirect

def profile(request):
    return render(request, 'app/mammoth/profile.html')

def mammothList(request):
    return render(request, 'app/mammoth/list.html')

def create(request):
    if request.method == 'POST':
        return redirect(request.POST['next'])
    return render(request, 'app/mammoth/profile.html')

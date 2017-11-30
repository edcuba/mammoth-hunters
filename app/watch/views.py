from django.shortcuts import render
from ..models import Watch


def watchList(request):
    context = {}

    watches = Watch.objects.all()

    context['watches'] = watches
    return render(request, 'app/watch/list.html', context)

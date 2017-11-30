from django.conf.urls import url
from .views import watchList

urlpatterns = [
    url(r'^list', watchList, name='watch_list')
]

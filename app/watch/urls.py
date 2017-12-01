from django.conf.urls import url
from .views import watchList, detail

urlpatterns = [
    url(r'^list', watchList, name='watch_list'),
    url(r'^detail', detail, name='watch_detail')
]

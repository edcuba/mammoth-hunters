from django.conf.urls import url
from .views import watchList, detail, end, create

urlpatterns = [
    url(r'^list', watchList, name='watch_list'),
    url(r'^detail', detail, name='watch_detail'),
    url(r'^create', create, name='watch_create'),    
    url(r'^end', end, name='watch_end')
]

from django.conf.urls import url
from .views import pitList, detail, lock

urlpatterns = [
    url(r'^$', pitList, name='pit_list'),
    url(r'^detail$', detail, name='pit_detail'),
    url(r'^lock$', lock, name='pit_lock')
]

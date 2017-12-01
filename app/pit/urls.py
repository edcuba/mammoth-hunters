from django.conf.urls import url
from .views import pitList

urlpatterns = [
    url(r'^', pitList, name='pit_list'),
    url(r'^create$', pitList, name='pit_create')
]

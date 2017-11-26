from django.conf.urls import url
from .views import huntList, detail

urlpatterns = [
    url(r'^list', huntList, name='hunt_list'),
    url(r'^detail', detail, name='hunt_detail')
]

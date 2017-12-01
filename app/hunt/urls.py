from django.conf.urls import url
from .views import huntList, detail

urlpatterns = [
    url(r'^list', huntList, name='hunt_list'),
    url(r'^detail', detail, name='hunt_detail'),
    url(r'^submit', detail, name='hunt_submit')
]

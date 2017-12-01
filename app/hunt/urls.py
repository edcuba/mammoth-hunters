from django.conf.urls import url
from .views import huntList, detail, add, submit

urlpatterns = [
    url(r'^list', huntList, name='hunt_list'),
    url(r'^detail', detail, name='hunt_detail'),
    url(r'^submit', submit, name='hunt_submit'),
    url(r'^add', add, name='hunt_add')
]

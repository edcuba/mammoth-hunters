from django.conf.urls import url, include
from .views import profile, mammothList, create, createInDash

urlpatterns = [
    url(r'^$', profile, name='mammoth_profile'),
    url(r'^create$', create, name='mammoth_create'),
    url(r'^createInDash$', createInDash, name='mammoth_dash_create'),
    url(r'^list', mammothList, name='mammoth_list')
]

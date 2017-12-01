from django.conf.urls import url, include
from .views import profile, mammothList, create

urlpatterns = [
    url(r'^$', profile, name='mammoth_profile'),
    url(r'^create$', create, name='mammoth_create'),
    url(r'^list', mammothList, name='mammoth_list')
]

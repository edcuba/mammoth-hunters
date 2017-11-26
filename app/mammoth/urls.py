from django.conf.urls import url, include
from .views import profile, mammothList

urlpatterns = [
    url(r'^$', profile, name='mammoth_profile'),
    url(r'^list', mammothList, name='mammoth_list')
]

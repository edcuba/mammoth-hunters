from django.conf.urls import url
from .views import profile, hunterList

urlpatterns = [
    url(r'^$', profile, name='hunter_profile'),
    url(r'^list', hunterList, name='hunter_list')
]

from django.conf.urls import url
from .views import profile, hunterList, changePass

urlpatterns = [
    url(r'^$', profile, name='hunter_profile'),
    url(r'^password', changePass, name='hunter_password'),
    url(r'^list', hunterList, name='hunter_list')
]

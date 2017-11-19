from django.conf.urls import url
from .views import requireLogin

urlpatterns = [
    url(r'^', requireLogin)
]

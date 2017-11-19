from django.conf.urls import url, include
from app import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login', include('app.login.urls'))
    #url(r'^.*\.html', views.gentella_html, name='gentella'),
]

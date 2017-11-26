from django.conf.urls import url, include
from app import views

urlpatterns = [
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^$', views.index, name='index'),
    url(r'^register', views.register, name='register'),
    url('^hunter', include('app.hunter.urls')),
    url('^mammoth', include('app.mammoth.urls')),
    url('^hunt', include('app.hunt.urls'))
]

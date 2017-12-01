from django.conf.urls import url
from .views import messageList, detail, create

urlpatterns = [
    url(r'^$', messageList, name='message_list'),
    url(r'^detail$', detail, name='message_detail'),
    url(r'^create$', create, name='message_create')
]

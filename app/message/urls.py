from django.conf.urls import url
from .views import messageList, detail

urlpatterns = [
    url(r'^$', messageList, name='message_list'),
    url(r'^detail$', detail, name='message_detail'),
]

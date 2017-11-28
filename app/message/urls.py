from django.conf.urls import url
from .views import messageList

urlpatterns = [
    url(r'^$', messageList, name='message_list'),
]

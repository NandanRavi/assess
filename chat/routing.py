from django.urls import re_path
from .consumers import ChatConsumer

websocket_urlpatterns = [
    re_path(r'ws/chat/sender/(?P<receiver_email>[^/]+)/$', ChatConsumer.as_asgi()),
    re_path(r'ws/chat/receiver/(?P<sender_email>[^/]+)/$', ChatConsumer.as_asgi()),
]

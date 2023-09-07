from django.urls import re_path
from django.urls.resolvers import URLPattern
from . import consumers
from typing import List

# Define the WebSocket URL patterns for the Django application.
# These patterns route WebSocket requests to the appropriate consumer classes.
websocket_urlpatterns: List[URLPattern] = [
    # re_path() creates a URL pattern for WebSocket connections.
    # The regular expression r"ws/chat/(?P<room_name>\w+)/$" captures a room name as a keyword argument.
    # The ChatConsumer.as_asgi() method reference routes the WebSocket request to the ChatConsumer class.
    re_path(r"ws/chat/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi()),
]

# synphony/routing.py
from django.urls import re_path

from . import consumers

# route to the consumer.
websocket_urlpatterns = [
    re_path(r'ws/synphony/(?P<key>\w+)/$', consumers.StudioConsumer),
]

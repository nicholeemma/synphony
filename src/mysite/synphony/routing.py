from django.urls import re_path
from django.urls import path
from django.conf.urls import url
from . import consumers

websocket_urlpatterns = [
	#path("ws/", consumers.EchoConsumer),
	url("^ws/synphony/(?P<key>[a-f0-9]{16})$", consumers.SyncConsumer)
]
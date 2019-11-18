
from django.urls import re_path
from django.conf.urls import url
from . import consumers

# route to the consumer.
websocket_urlpatterns = [
	url("^ws/sync/synphony/(?P<key>[a-f0-9]{16})$", consumers.SyncConsumer),
    re_path(r'ws/synphony/(?P<key>\w+)/$', consumers.StudioConsumer)
]

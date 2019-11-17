# mysite/routing.py
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path

from synphony.consumers import EchoConsumer

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    "websocket": URLRouter([
        path("ws/", EchoConsumer)
    ])
})

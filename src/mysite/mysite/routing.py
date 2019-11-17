# mysite/routing.py
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import synphony.routing

# point the root routing configuration at the chat.routing module.
application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            synphony.routing.websocket_urlpatterns
        )
    ),
})

from channels.routing import ProtocolTypeRouter,URLRouter
from channels.auth import AuthMiddlewareStack
import ChatApp.routing
application = ProtocolTypeRouter({
    'websocket':AuthMiddlewareStack(
        URLRouter(
            ChatApp.routing.websocket_urlpatterns 
        )
    )
})
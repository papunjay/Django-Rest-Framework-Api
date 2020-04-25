from channels.routing import ProtocolTypeRouter,URLRouter
from channels.auth import AuthMiddlewareStack
import ChatApp.routing
#import peer_to_peer_ChatApp.routing
application = ProtocolTypeRouter({
    'websocket':AuthMiddlewareStack(
        URLRouter
        (
            ChatApp.routing.websocket_urlpatterns, 
            #peer_to_peer_ChatApp.routing.websocket_urlpatterns

        )
    )
})
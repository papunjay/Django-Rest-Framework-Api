
from django.contrib import admin
from django.urls import path,include
from User import views 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('chat/', include('ChatApp.urls')),
    path('', include('User.urls')),
    path('p2p_chat/',include('peer_to_peer_ChatApp'))
]

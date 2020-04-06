from django.urls import path,include
from  User.views import Registration,Home,Login,welcome
from django.contrib import admin
from User.serializers import RegistrationSerializers

urlpatterns = [
    path('home/',Home.as_view(),name='home'),
    path('register/',Registration.as_view(),name='register'),
    path('login/',Login.as_view(),name='login'),
    path('admin/', admin.site.urls),
    path('welcome/',welcome.as_view(),name='welcome'),
  
]
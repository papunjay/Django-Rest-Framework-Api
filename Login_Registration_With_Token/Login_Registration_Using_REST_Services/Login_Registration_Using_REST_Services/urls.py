from django.contrib import admin
from django.urls import path,include
from User import views 
#from  User.views import Registration,Home,Login,welcome

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('User.urls')),
    #path('register/',Registration.as_view(),name='register'),
]

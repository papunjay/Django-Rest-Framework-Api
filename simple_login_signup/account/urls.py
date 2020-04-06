from django.urls import path,include
from account import views
from django.contrib import admin

urlpatterns = [
    path('home/',views.home,name='home'),
    path('signup/',views.signup,name='signup'),
    path('login/',views.login_page,name='login'),
    path('admin/', admin.site.urls),
]

from django.urls import path,include
from  User.views import Registration,Home,Login,welcome
from django.contrib import admin
from User.serializers import RegistrationSerializers
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views
from rest_framework_jwt import views as jwt_views
from django.conf.urls import include, url

urlpatterns = [
    path('home', views.home, name='home'),
    path('registration/', views.Registrations.as_view(), name="registration"),

    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', views.Login.as_view(), name="login"),
    path('forgotpassword', views.ForgotPassword.as_view(),name="forgotPassword"),
    path('activate/<surl>/', views.activate, name="activate"),
    path('reset_password/<surl>/', views.reset_password, name="reset_password"),
    path('resetpassword/<user_reset>', views.ResetPassword.as_view(), name="resetpassword"),
    path('logout/', views.Logout.as_view() ,name="logout"),

]

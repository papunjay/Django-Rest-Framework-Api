from django.urls import path,include
from django.urls import path,include
from  User.views import Registration,Login,Home,welcome,activate,reset_password,ResetPassword,ForgotPassword,logout
from django.contrib import admin
from User.serializers import RegistrationSerializers
from rest_framework_jwt.views import refresh_jwt_token, obtain_jwt_token

urlpatterns = [

    path('home/',Home.as_view(),name='home'),
    path('register/',Registration.as_view(),name='register'),
    path('activate/<slug:surl>',activate, name='activate'),
    path('login/',Login.as_view(),name='login'),
    path('forgotpassword/',ForgotPassword.as_view(),name="forgotpassword"),
]
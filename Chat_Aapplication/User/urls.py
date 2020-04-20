from django.urls import path,include
from  User.views import Registration,Login,Home,welcome,activate,reset_password,ResetPassword,ForgotPassword,logout
from django.contrib import admin
from User.serializers import RegistrationSerializers
from rest_framework_jwt.views import refresh_jwt_token, obtain_jwt_token

urlpatterns = [
    path('home/',Home.as_view(),name='home'),
    path('register/',Registration.as_view(),name='register'),
    path('login/',Login.as_view(),name='login'),
    path('admin/', admin.site.urls),
    path('welcome/',welcome.as_view(),name='welcome'),
    path('activate/<slug:surl>',activate, name='activate'),
    path('forgotpassword/',ForgotPassword.as_view(),name="forgotpassword"),
    path('reset_password/<slug:surl>/', reset_password, name="reset_password"),
    path('logout/',logout, name='activate'),
    path('resetpassword/<user_reset>/',ResetPassword.as_view(), name="resetpassword"),
    
    # path('auth/jwt/', obtain_jwt_token),
    # path('auth/jwt/refresh', refresh_jwt_token),

]
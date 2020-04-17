from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import UsersData
from django.contrib.auth import login, logout
from django.db.models import Q
from rest_framework.generics import GenericAPIView
from .serializers import (RegistrationSerializers,LoginSerializers,ResetSerializers)
from rest_framework import authentication, permissions
from django.contrib.auth import authenticate, get_user_model
from django.views.generic import TemplateView
from User.token import token_activation
from django.contrib.sites.shortcuts import get_current_site
from django_short_url.views import get_surl
from django_short_url.models import ShortURL
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
User = get_user_model()
import json
from Login_Registration_Using_REST_Services.settings import SECRET_KEY
from django.contrib.auth.models import User,auth
from django.contrib.auth import login, logout
import jwt

class Home(TemplateView):
    template_name = 'home.html'


class welcome(TemplateView):
    template_name = 'welcome.html'



class Registration(GenericAPIView):
    serializer_class = RegistrationSerializers
    def get(self, request):
        return render(request,'Registration/signup.html')
        
    def post(self, request):
        if request.user.is_authenticated:
            
            return HttpResponse("your are already registred,please do login")
        data = request.POST
        username = data.get('username')
        email = data.get('email')
        password1 = data.get('password1')
        password2 = data.get('password2')
        if password1 != password2:
            return HttpResponse("passwords are not matching")
            
        qs_name = User.objects.filter(
            Q(username__iexact=username)
        )
        qs_email = User.objects.filter(
            Q(email__iexact=email)
        )
        if qs_name.exists():
            return HttpResponse("already user id pret with this username ")
            
        elif qs_email.exists():
            return HttpResponse("already user id present with this  email")
            
        else:
            user = User.objects.create(username=username, email=email)
            user.set_password(password1)
            user.is_active = False
            user.save()

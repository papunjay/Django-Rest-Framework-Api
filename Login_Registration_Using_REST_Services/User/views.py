from django.http import HttpResponse,Http404
from rest_framework.views import APIView
from django.shortcuts import render, redirect
from .models import UsersData
from rest_framework.authentication import authenticate
from rest_framework.response import Response
from django.contrib.auth import login, logout
from django.db.models import Q
from rest_framework.generics import api_settings
from rest_framework.generics import GenericAPIView
from .serializers import (RegistrationSerializers,LoginSerializers,)
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth import authenticate, get_user_model
from django.views.generic import TemplateView
from django.contrib import messages
User = get_user_model()


class Home(TemplateView):
    template_name = 'home.html'


class welcome(TemplateView):
    template_name = 'welcome.html'


class Login(GenericAPIView):
    serializer_class = LoginSerializers

    def get(self,request):
        return render(request,'Login/login.html')

    def post(self, request):
        permission_classes = [permissions.AllowAny]
        if request.user.is_authenticated :
            return HttpResponse({'details': 'user is already authenticated'})
        data = request.POST
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)
        print(username,password)
        qs = User.objects.filter(
            Q(username__iexact=username) or
            Q(password__iexact=password)
        ).distinct()
        if qs.count() == 1:
            user_obj = qs.first()
            if user_obj.check_password(password):
                user = user_obj
                login(request, user,backend='django.contrib.auth.backends.ModelBackend')
                return Response('login')
            return HttpResponse("check password again")
        return HttpResponse("multiple users are present with this username")



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
        # if len(password1) < 4 or len(password2) <4:
        #     return HttpResponse("length of the password must be greater than 4") 
            
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
            return HttpResponse("ragistration complited")
    
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

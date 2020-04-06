from django.http import HttpResponse
from rest_framework.views import APIView
from django.shortcuts import render, redirect
from .models import Registration
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
User = get_user_model()
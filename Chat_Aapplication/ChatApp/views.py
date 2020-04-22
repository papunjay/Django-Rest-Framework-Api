from django.shortcuts import render
import json
from django.utils.safestring import mark_safe
# Create your views here.

def index(request):
    return render(request, 'chat/index.html')

def room(request,room_name,person_name):
    return render(request,"chat/room.html",{'room_name':room_name,'person_name':person_name})
  
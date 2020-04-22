import asyncio
import json
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from .models import thread,ChatMessage


class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self,event):
        print("connected",event)
    
  

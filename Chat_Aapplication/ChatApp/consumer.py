from channels.generic.websocket import WebsocketConsumer
import json
from asgiref.sync import async_to_sync

class ChatConsumer(WebsocketConsumer):
     def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()
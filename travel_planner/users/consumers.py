import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone
from .models import UserActivity

class UserActivityConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'user_activity'
        
        # Join room group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        
        await self.accept()
    
    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
    
    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        
        # Send message to room group
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'user_activity_message',
                'message': message
            }
        )
    
    # Receive message from room group
    async def user_activity_message(self, event):
        message = event['message']
        
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
        
    @database_sync_to_async
    def log_activity(self, user_id, action, ip_address, page_visited):
        UserActivity.objects.create(
            user_id=user_id,
            action=action,
            ip_address=ip_address,
            page_visited=page_visited,
            timestamp=timezone.now()
        ) 
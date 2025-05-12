import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone

class BookingUpdatesConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'booking_updates'
        
        # Join booking updates group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        
        await self.accept()
    
    async def disconnect(self, close_code):
        # Leave booking updates group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
    
    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        booking_id = text_data_json.get('booking_id')
        status = text_data_json.get('status')
        
        # Send message to booking updates group
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'booking_update',
                'message': message,
                'booking_id': booking_id,
                'status': status
            }
        )
    
    # Receive message from booking updates group
    async def booking_update(self, event):
        message = event['message']
        booking_id = event.get('booking_id')
        status = event.get('status')
        
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'booking_id': booking_id,
            'status': status,
            'timestamp': timezone.now().isoformat()
        })) 
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Ride

class RideTrackingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.ride_id = self.scope['url_route']['ride_id']
        
        # Join room group
        await self.channel_layer.group_add(
            f"ride_{self.ride_id}",
            self.channel_name
        )
        
        await self.accept()
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            f"ride_{self.ride_id}",
            self.channel_name
        )
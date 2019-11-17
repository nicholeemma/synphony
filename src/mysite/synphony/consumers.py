# synphony/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json


class StudioConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.key = self.scope['url_route']['kwargs']['key']
        self.studio_group_name = '%s' % self.key
        # Join room group
        # await is used to call asynchronous functions that perform I/O.
        await self.channel_layer.group_add(
            self.studio_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.studio_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.studio_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))


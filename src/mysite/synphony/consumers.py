
from channels.generic.websocket import WebsocketConsumer
from channels.consumer import AsyncConsumer
import json

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        self.send(text_data=json.dumps({
            'message': message
        }))


class EchoConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        await self.send({
            "type": "websocket.accept"
        })
    
    async def websocket_recieve(self, event):
        await self.send({
            "type": "websocket.send",
            "text": event["text"]
        })

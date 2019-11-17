
from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
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


class SyncConsumer(AsyncWebsocketConsumer):
	async def connect(self):

		self.studio_name = self.scope['url_route']['kwargs']['key']
		self.studio_group_name = 'studio_%s' % self.studio_name

		# Join room group
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
		msg_type = text_data_json['msg_type']
		msg_content = text_data_json['msg_content']
		
		print(msg_type)

		# Send message to room group
		await self.channel_layer.group_send(
			self.studio_group_name,
			{
				'type': 'sync_message',
				'msg_type' : msg_type,
				'msg_content': msg_content
			}
		)

	# Receive message from room group
	async def sync_message(self, event):
		msg_type = event['msg_type']
		msg_content = event['msg_content']

		# Send message to WebSocket
		await self.send(text_data=json.dumps({
			'msg_type' : msg_type,
			'msg_content': msg_content
		}))
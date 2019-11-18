# synphony/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Studio, Music, Participant, Comment, History
from django.contrib.auth.models import User
import json


class StudioConsumer(AsyncWebsocketConsumer):
    async def connect(self, event=''):
        self.key = self.scope['url_route']['kwargs']['key']
        self.studio_group_name = '%s' % self.key
         # login the user to this session.
        # save the session (if the session backend does not access the db you can use `sync_to_async`)
        
        # Join room group
        # await is used to call asynchronous functions that perform I/O.
        await self.channel_layer.group_add(
            self.studio_group_name,
            self.channel_name
        )
        await self.store_participant()
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
        self.message = message
        print(message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.studio_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': self.scope["user"]
            }
        )

        await self.store_comment()

    @database_sync_to_async
    def store_comment(self):
        # acquire the current studio
        cur_studio = Studio.objects.get(link__exact=self.key)
        commentcontent = self.message
        user_name = self.message.split(':', 2)[0]
        commentuser = User.objects.get(username__exact=user_name)
        new_comment = Comment(user_name=commentuser, text=commentcontent, commented_on=cur_studio)
        new_comment.save()
        print("comment saved!")

    @database_sync_to_async
    def store_participant(self):
        # acquire the current studio
        cur_studio = Studio.objects.get(link=self.key)
        print(cur_studio)
        user_name = self.scope["user"]
        cur_user = User.objects.get(username=user_name)
        print(Participant.objects.filter(participant_user=cur_user))
        print(Participant.objects.filter(participant_user=cur_user, studio=cur_studio))
        # if (Participant.objects.filter(participant_user=cur_user) not in Participant.objects.filter(participant_user=cur_user, studio=cur_studio)) or (Participant.objects.filter(participant_user=cur_user, studio=cur_studio) is None):
        new_p = Participant(participant_user=cur_user, studio=cur_studio)
        new_p.save()
        print("p saved!")

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

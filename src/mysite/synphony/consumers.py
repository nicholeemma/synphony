
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Studio, Music, Participant, Comment, History
from django.forms.models import model_to_dict
from .forms import MusicForm
from django.contrib.auth.models import User
import json


class SyncConsumer(AsyncWebsocketConsumer):
    async def connect(self):

        self.studio_name = self.scope['url_route']['kwargs']['key']
        self.studio_group_name = 'studio_%s' % self.studio_name

        # Join studio group
        await self.channel_layer.group_add(
            self.studio_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave studio group
        await self.channel_layer.group_discard(
            self.studio_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        msg_type = text_data_json['msg_type']
        msg_content = text_data_json['msg_content']

        # Send message to studio group
        await self.channel_layer.group_send(
            self.studio_group_name,
            {
                'type': 'sync_message',
                'msg_type': msg_type,
                        'msg_content': msg_content
            }
        )

    # Receive message from studio group
    async def sync_message(self, event):
        msg_type = event['msg_type']
        msg_content = event['msg_content']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'msg_type': msg_type,
            'msg_content': msg_content
        }))


class PlaylistConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.key = self.scope['url_route']['kwargs']['key']
        self.playlist_group_name = 'playlist_%s' % self.key
        # Join playlist group
        # await is used to call asynchronous functions that perform I/O.
        await self.channel_layer.group_add(
            self.playlist_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.playlist_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print("message received")
        msg_type = text_data_json['msg_type']
        msg_content = text_data_json['msg_content']
        rsp = dict()
        # check music info
        if msg_type == 'add_song':
            try:
                studio = Studio.objects.get(link__exact=self.key)
            except:
                rsp = {"error": "form not valid!"}
            music_form = MusicForm(msg_content)
            if(music_form.is_valid()):
                music = music_form.save()
                studio.music.add(music)
                rsp = model_to_dict(music)
            else:
                rsp = {"error": "form not valid!"}
                print("forms not valid!")
        if msg_type == 'remove_song':
            try:
                cur_studio = Studio.objects.get(link__exact=self.key)
            except:
                rsp = {"error": "form not valid!"}
            music_id = msg_content['id']
            music_set = Music.objects.filter(pk=music_id)
            rsp = msg_content
            if music_set.count() > 0:
                music = Music.objects.get(pk=music_id)
                # check if music in cur_studio
                if cur_studio.music.filter(pk=music_id).count() > 0:
                    cur_studio.music.remove(music)

        # Send message to playlist group
        await self.channel_layer.group_send(
            self.playlist_group_name,
            {
                'type': 'sync_message',
                'msg_type': msg_type,
                'msg_content': rsp
            }
        )

    # Receive message from playlist group
    async def sync_message(self, event):
        msg_type = event['msg_type']
        msg_content = event['msg_content']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'msg_type': msg_type,
            'msg_content': msg_content
        }))


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
        self.message = message
        print(message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.studio_group_name,
            {
                'type': 'chat_message',
                'message': message
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

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

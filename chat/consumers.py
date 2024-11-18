from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
import json
from .models import Message
from users.models import CustomUser
from users.utils import decode_jwt

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        token = self.scope['query_string'].decode().split('=')[-1]
        self.scope['user'] = await self.authenticate_user(token)

        if self.scope['user'] is None or self.scope['user'].is_anonymous:
            await self.close()
            return

        if 'receiver_email' in self.scope['url_route']['kwargs']:
            self.role = 'sender'
            self.counterpart_email = self.scope['url_route']['kwargs']['receiver_email']
        elif 'sender_email' in self.scope['url_route']['kwargs']:
            self.role = 'receiver'
            self.counterpart_email = self.scope['url_route']['kwargs']['sender_email']
        else:
            self.role = None
            self.counterpart_email = None

        self.counterpart_user = await self.get_user(self.counterpart_email)

        if self.counterpart_user:
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        if not self.scope['user'].is_anonymous:
            print(f"Disconnected: {self.scope['user'].email}")

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            message = data.get('message')

            if self.role == 'sender':
                await self.save_message(self.scope['user'], self.counterpart_user, message)
            elif self.role == 'receiver':
                await self.save_message(self.counterpart_user, self.scope['user'], message)

            await self.send(text_data=json.dumps({
                'message': message,
                'sender': self.scope['user'].email,
            }))
        except Exception as e:
            print(f"Error in receive: {e}")

    @staticmethod
    @database_sync_to_async
    def get_user(email):
        try:
            return CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return None

    @staticmethod
    @database_sync_to_async
    def save_message(sender, receiver, content):
        return Message.objects.create(
            sender=sender,
            receiver=receiver,
            content=content,
        )

    async def authenticate_user(self, token):
        try:
            payload = decode_jwt(token)
            user = await self.get_user_by_id(payload['user_id'])
            return user
        except Exception as e:
            print(f"Authentication failed: {e}")
            return AnonymousUser()

    @staticmethod
    @database_sync_to_async
    def get_user_by_id(user_id):
        """Fetch user by ID synchronously."""
        try:
            return CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return None

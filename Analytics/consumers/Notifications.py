import json
from channels.db import sync_to_async
from channels.exceptions import StopConsumer
import jwt
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from ..models.Notifications import Notification
from ..models.Account import Account
from django.conf import settings



class NotificationsCountConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.accept()


    async def disconnect(self, close_code):
        raise StopConsumer()


    async def receive(self, text_data):
        data = json.loads(text_data)

        tok = data['token']

        try:
            tok = jwt.decode(tok, settings.SECRET_KEY, "HS256")

            user_id = tok['user_id']

            user = await sync_to_async(Account.objects.all().filter(pk=user_id).first)()

            instance = await sync_to_async(Notification.objects.all().filter(account=user.username, isRead=False).count)()

            await self.send(text_data=json.dumps({"status": 0, "data": {"count": instance}}))


        except jwt.ExpiredSignatureError as error:
            await self.send(text_data=json.dumps({"status": -1, "data": f"signature verification failed: {error}"}))

        except Exception:
            await self.send(text_data=json.dumps({"status": -1, "data": ""}))




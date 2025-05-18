import json
from channels.exceptions import StopConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
from rest_framework.authtoken.models import Token
from ..models.Notifications import Notification
from channels.db import database_sync_to_async


@database_sync_to_async
def get_user(token):
    try:
        tok = Token.objects.filter(key=token).first()
        if tok and tok.user:
            return tok.user
    except Exception:
        return None


@database_sync_to_async
def get_unread(user):
    try:
        return Notification.objects.filter(account=user, isRead=False).count()
    except Exception:
        return 0


class NotificationsCountConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        subprotocols = self.scope.get("subprotocols", [])
        token = subprotocols[0] if subprotocols else None

        if not token:
            await self.close()

        self.user = await get_user(token)

        if not self.user or not self.user.is_authenticated:
            await self.close()

        await self.accept(token)

        await self.send_unread_count()



    async def disconnect(self, close_code):
        raise StopConsumer()


    async def send_unread_count(self):
        try:

            unread_notifications = await get_unread(self.user)



            await self.send(text_data=json.dumps({
                    "count": unread_notifications
                }))


        except Exception:
            self.close()


    async def receive(self, text_data=None):
        try:
            unread_notifications = await get_unread(self.user)


            await self.send(text_data=json.dumps({
                    "count": unread_notifications
                }))
        except Exception:
            self.close()


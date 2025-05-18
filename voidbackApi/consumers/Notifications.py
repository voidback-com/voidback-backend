import json
from channels.generic.websocket import AsyncWebsocketConsumer
from rest_framework.authtoken.models import Token
from ..models.Notifications import Notification
from channels.db import database_sync_to_async



@database_sync_to_async
def get_user(token):
    try:
        tok = Token.objects.all().filter(key=token).first()

        if tok.user:
            return tok.user
    except Exception:
        return None



@database_sync_to_async
def get_unread(user):
    try:
        return Notification.objects.all().filter(account=user.username, isRead=False).count()
    except Exception:
        pass



class NotificationsCountConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        subprotocols = self.scope.get("subprotocols", [])
        token = None

        if subprotocols:
            token = subprotocols[0]

        if token:
            self.user = await get_user(token)

            if self.user and self.user.is_authenticated:

                self.room_name = f"notifications-{self.user.id}"
                self.room_group_name = "notifications"

                # join the room specific to user
                await self.channel_layer.group_add(
                    self.room_group_name,
                    self.channel_name
                )

                await self.channel_layer.group_add(
                    self.room_name,
                    self.channel_name
                )

                await self.accept() # user connected to the room


                # send initial unread notifications after user connection
                unread_notifications = await get_unread(self.user)

                await self.send(text_data=json.dumps({
                    "count": unread_notifications
                }))

            else:
                await self.close()

        else:
            await self.close()




    async def disconnect(self, close_code):
        if hasattr(self, "room_group_name"):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

        if hasattr(self, 'room_name'):
            await self.channel_layer.group_discard(
                self.room_name,
                self.channel_name
            )

        # raise StopConsumer()


    
    # handles sending the unread notifications count to the user
    async def send_unread(self, event):
        count = event['count']

        await self.send(text_data=json.dumps({
            "count": count
        }));



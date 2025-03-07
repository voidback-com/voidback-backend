import json
from channels.db import sync_to_async
from channels.exceptions import StopConsumer
from django.db.models import Q
from django.utils.timezone import timedelta
import jwt
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from ..models.DirectMessage import DirectMessageSession, DMMessage
from ..serializers.DirectMessage import DMMessageSerializer
from ..models.Account import Account
from django.conf import settings
from django.utils import timezone


class LiveDirectMessageConsumer(WebsocketConsumer):

    def connect(self):
        self.accept()


    def disconnect(self, close_code):
        raise StopConsumer()


    def receive(self, text_data):
        try:
            data = json.loads(text_data)
            tok = data['token']
            sessionID = data['sessionID']

            tok = jwt.decode(tok, settings.SECRET_KEY, "HS256")

            user_id = tok['user_id']


            message = DMMessage.objects.all().filter(session__id=sessionID, seen=False).exclude(sender__id=user_id).last()


            # verify the user_id is apart of this dm session

            if message and message.session.initiator.id!=user_id and message.session.friend.id!=user_id:
                self.send(text_data=json.dumps({"status": -1, "data": ""}))

            
            # else:
            if message and message.sender.id==user_id:
                self.send(text_data=json.dumps({"status": -1, "data": ""}))

            elif message:
                message.seen = True
                message.save()

                serialized = DMMessageSerializer(message)

                self.send(text_data=json.dumps({"status": 0, "data": serialized.data}))


        except jwt.ExpiredSignatureError as error:
            self.send(text_data=json.dumps({"status": -1, "data": f"signature verification failed: {error}"}))

        except Exception:
            self.send(text_data=json.dumps({"status": -1, "data": ""}))




import json
from channels.db import sync_to_async
from channels.exceptions import StopConsumer
import jwt
from channels.generic.websocket import WebsocketConsumer
from rest_framework.authtoken.models import Token
from ..models.Notifications import Notification
from ..models.Account import Account
from django.conf import settings



class NotificationsCountConsumer(WebsocketConsumer):

    def connect(self):
        self.accept()


    def disconnect(self, close_code):
        raise StopConsumer()


    def receive(self, text_data):
        try:
            data = json.loads(text_data)
            tok = data['token']


            user_id = Token.objects.all().filter(key=tok).first()


            if user_id:
                user_id = user_id.user.id


            user = Account.objects.all().filter(pk=user_id).first()

            instance = Notification.objects.all().filter(account=user.username, isRead=False).count()

            self.send(text_data=json.dumps({"status": 0, "data": {"count": instance}}))


        except Exception:
            self.send(text_data=json.dumps({"status": -1, "data": ""}))




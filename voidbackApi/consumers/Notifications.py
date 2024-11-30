import json
import jwt
from channels.generic.websocket import WebsocketConsumer
from ..models.Notifications import Notification
from ..models.Account import Account
from django.conf import settings



class NotificationsCountConsumer(WebsocketConsumer):

    def connect(self):
        self.accept()


    def disconnect(self, close_code):
        self.close()


    def receive(self, text_data):
        data = json.loads(text_data)

        tok = data['token']

        try:
            tok = jwt.decode(tok, settings.SECRET_KEY, "HS256")

            user_id = tok['user_id']

            user = Account.objects.all().filter(pk=user_id).first()

            instance = Notification.objects.all().filter(account=user.username, isRead=False).count()

            self.send(text_data=json.dumps({"status": 0, "data": {"count": instance}}))


        except jwt.ExpiredSignatureError as error:
            self.send(text_data=json.dumps({"status": -1, "data": f"signature verification failed: {error}"}))

        except KeyboardInterrupt:
            self.send(text_data=json.dumps({"status": -1, "data": ""}))




import json
from channels.db import sync_to_async
from channels.exceptions import StopConsumer
import jwt
from channels.generic.websocket import WebsocketConsumer
from voidbackApi.models.Account import Account
from ..models import Event
from django.conf import settings
from django.utils import timezone



class NegativeEventsConsumer(WebsocketConsumer):

    def connect(self):
         self.accept()


    def disconnect(self, close_code):
        raise StopConsumer()


    def receive(self, text_data):


        try:
            data = json.loads(text_data)

            tok = data['token']

            today = timezone.now()
            start_date = timezone.datetime(year=today.year, month=today.month, day=today.day, hour=0, minute=0, second=0)
            end_date = timezone.datetime(year=today.year, month=today.month, day=today.day, hour=23, minute=59, second=59)


            user = Account.objects.all().filter(pk=user_id).first()

            if not user.is_staff:
                 self.send(text_data={"status": -1, "data": "unauthorized"})



            deleted_posts = Event.objects.all().filter(
                event_type="delete-post",
                created_at__range=[start_date, end_date]
          ).count()


            unlike_posts = Event.objects.all().filter(
                event_type="unlike-post",
                created_at__range=[start_date, end_date]
          ).count()


            dislike_posts =  Event.objects.all().filter(
                event_type="dislike-post",
                created_at__range=[start_date, end_date]
          ).count()


            deleted_research =  Event.objects.all().filter(
                event_type="delete-research-paper",
                created_at__range=[start_date, end_date]
          ).count()

            research_reports = Event.objects.all().filter(
                event_type="submit-research-report",
                created_at__range=[start_date, end_date]
          ).count()


            posts_reports = Event.objects.all().filter(
                event_type="view-myresearch",
                created_at__range=[start_date, end_date]
          ).count()

            data = {
                "deleted_posts": deleted_posts,
                "unliked_posts": unlike_posts,
                "disliked_posts": dislike_posts,
                "deleted_research": deleted_research,
                "research_reports": research_reports,
                "post_reports": posts_reports
            }

            self.send(text_data=json.dumps({"status": 0, "data": data}))


        except jwt.ExpiredSignatureError as error:
             self.send(text_data=json.dumps({"status": -1, "data": f"signature verification failed: {error}"}))

        except Exception:
             self.send(text_data=json.dumps({"status": -1, "data": ""}))




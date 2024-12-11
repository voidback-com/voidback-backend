import json
from channels.db import sync_to_async
from channels.exceptions import StopConsumer
import jwt
from channels.generic.websocket import AsyncWebsocketConsumer
from voidbackApi.models.Account import Account
from ..models import Event
from django.conf import settings
from django.utils import timezone



class PositiveEventsConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.accept()


    async def disconnect(self, close_code):
        raise StopConsumer()


    async def receive(self, text_data):


        try:
            data = json.loads(text_data)

            tok = data['token']

            today = timezone.now()
            start_date = timezone.datetime(year=today.year, month=today.month, day=today.day, hour=0, minute=0, second=0)
            end_date = timezone.datetime(year=today.year, month=today.month, day=today.day, hour=23, minute=59, second=59)

            tok = jwt.decode(tok, settings.SECRET_KEY, "HS256")

            user_id = tok['user_id']

            user = await sync_to_async(Account.objects.all().filter(pk=user_id).first)()

            if not user.is_staff:
                await self.send(text_data={"status": -1, "data": "unauthorized"})



            view_posts = await sync_to_async(Event.objects.all().filter(
                event_type="view-post",
                created_at__range=[start_date, end_date]
          ).count)()


            liked_posts = await sync_to_async(Event.objects.all().filter(
                event_type="like-post",
                created_at__range=[start_date, end_date]
          ).count)()


            new_posts = await sync_to_async(Event.objects.all().filter(
                event_type="new-post",
                created_at__range=[start_date, end_date]
          ).count)()


            view_account_posts = await sync_to_async(Event.objects.all().filter(
                event_type="view-account-post",
                created_at__range=[start_date, end_date]
          ).count)()

            view_account_liked_posts = await sync_to_async(Event.objects.all().filter(
                event_type="view-account-liked-posts",
                created_at__range=[start_date, end_date]
          ).count)()


            view_myresearch = await sync_to_async(Event.objects.all().filter(
                event_type="view-myresearch",
                created_at__range=[start_date, end_date]
          ).count)()


            view_research = await sync_to_async(Event.objects.all().filter(
                event_type="view-research-paper",
                created_at__range=[start_date, end_date]
          ).count)()


            make_research_impression = await sync_to_async(Event.objects.all().filter(
                event_type="view-research-paper",
                created_at__range=[start_date, end_date]
          ).count)()




            data = {
                "posts_viewed": view_posts,
                "liked_posts": liked_posts,
                "new_posts": new_posts,
                "view_account_posts": view_account_posts,
                "view_account_liked_posts": view_account_liked_posts,
                "view_myresearch": view_myresearch,
                "view_research": view_research,
                "make_research_impression": make_research_impression
            }


            await self.send(text_data=json.dumps({"status": 0, "data": data}))


        except jwt.ExpiredSignatureError as error:
            await self.send(text_data=json.dumps({"status": -1, "data": f"signature verification failed: {error}"}))

        except Exception:
            await self.send(text_data=json.dumps({"status": -1, "data": ""}))




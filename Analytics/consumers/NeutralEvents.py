import json
from channels.db import sync_to_async
from channels.exceptions import StopConsumer
import jwt
from channels.generic.websocket import AsyncWebsocketConsumer
from voidbackApi.models.Account import Account
from ..models import Event
from django.conf import settings
from django.utils import timezone



class NeutralEventsConsumer(AsyncWebsocketConsumer):

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



            explore_queries = await sync_to_async(Event.objects.all().filter(
                event_type="explore-search-query",
                created_at__range=[start_date, end_date]
          ).count)()


            explore_category_queries = await sync_to_async(Event.objects.all().filter(
                event_type="explore-category-search-query",
                created_at__range=[start_date, end_date]
          ).count)()


            search_queries = await sync_to_async(Event.objects.all().filter(
                event_type="search-query",
                created_at__range=[start_date, end_date]
          ).count)()


            research_queries = await sync_to_async(Event.objects.all().filter(
                event_type="search-papers",
                created_at__range=[start_date, end_date]
          ).count)()


            data = {
                "explore_queries": explore_queries,
                "explore_category_queries": explore_category_queries,
                "search_queries": search_queries,
                "research_queries": research_queries
            }

            await self.send(text_data=json.dumps({"status": 0, "data": data}))


        except jwt.ExpiredSignatureError as error:
            await self.send(text_data=json.dumps({"status": -1, "data": f"signature verification failed: {error}"}))

        except Exception:
            await self.send(text_data=json.dumps({"status": -1, "data": ""}))




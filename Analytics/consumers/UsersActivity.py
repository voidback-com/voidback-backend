from hashlib import sha256
import json
from channels.db import sync_to_async
from channels.exceptions import StopConsumer
import jwt
from channels.generic.websocket import AsyncWebsocketConsumer
from Analytics.serializers import DeviceSerializer
from voidbackApi.models.Account import Account
from ..models import Event, Device, UsersActivityHistory
from django.conf import settings
from django.utils import timezone
from django.core import serializers



class UsersActivityConsumer(AsyncWebsocketConsumer):

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


            logouts_today = await sync_to_async(Event.objects.all().filter(
                event_type="auth-logout",
                created_at__range=[start_date, end_date]
          ).count)()

            otps_sent_today = await sync_to_async(Event.objects.all().filter(
                event_type="auth-send-otp",
                created_at__range=[start_date, end_date]
          ).count)()

            otps_verified_today = await sync_to_async(Event.objects.all().filter(
                event_type="auth-verify-otp",
                created_at__range=[start_date, end_date]
          ).count)()

            logins_today = await sync_to_async(Event.objects.all().filter(
                event_type="auth-login",
                created_at__range=[start_date, end_date]
          ).count)()

            deleted_accounts_today = await sync_to_async(Event.objects.all().filter(
                event_type="auth-delete-account",
                created_at__range=[start_date, end_date]
          ).count)()


            updated_accounts_today = await sync_to_async(Event.objects.all().filter(
                event_type="auth-account-update",
                created_at__range=[start_date, end_date]
          ).count)()

            follows_today = await sync_to_async(Event.objects.all().filter(
                event_type="auth-follow",
                created_at__range=[start_date, end_date]
          ).count)()


            unfollows_today = await sync_to_async(Event.objects.all().filter(
                event_type="auth-unfollow",
                created_at__range=[start_date, end_date]
          ).count)()


            account_reports_today = await sync_to_async(Event.objects.all().filter(
                event_type="auth-account-report",
                created_at__range=[start_date, end_date]
          ).count)()


            signups_today = await sync_to_async(Event.objects.all().filter(
                event_type="auth-signup",
                created_at__range=[start_date, end_date]
          ).count)()


            countries_today = await sync_to_async(Device.objects.all().filter(
                created_at__range=[start_date, end_date]
            ).values("country").distinct)()

            countries_today = await sync_to_async(list)(countries_today)
 

            cities_today = await sync_to_async(Device.objects.all().filter(
                created_at__range=[start_date, end_date]
            ).values("city").distinct)()

            cities_today = await sync_to_async(list)(cities_today)


            data = {
                "logouts": logouts_today,
                "otps_sent": otps_sent_today,
                "otps_verified": otps_verified_today,
                "logins": logins_today,
                "deleted_accounts": deleted_accounts_today,
                "updated_accounts": updated_accounts_today,
                "follows": follows_today,
                "unfollows": unfollows_today,
                "account_reports_today": account_reports_today,
                "signups": signups_today,
                "countries": countries_today,
                "cities": cities_today,
                "dateRange": [start_date.timestamp(), end_date.timestamp()]
            }


            s = await sync_to_async(str)(data)

            sdat = await sync_to_async(s.encode)()

            hash = await sync_to_async(sha256(sdat).hexdigest)()

            hist = await sync_to_async(UsersActivityHistory.objects.all().filter(hash=hash).first)()

            if not hist:
                hist = await sync_to_async(UsersActivityHistory(data=data, hash=hash).save)()


            await self.send(text_data=json.dumps({"status": 0, "data": data}))


        except jwt.ExpiredSignatureError as error:
            await self.send(text_data=json.dumps({"status": -1, "data": f"signature verification failed: {error}"}))

        except Exception:
            await self.send(text_data=json.dumps({"status": -1, "data": ""}))




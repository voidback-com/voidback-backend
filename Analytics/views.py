from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from django.utils import timezone
from django.contrib.gis.geoip2 import GeoIP2
from voidbackApi.models.Post import Hashtag, Symbol
from .serializers import EventSerializer, Event
from .models import Device
import urllib.request



def getDevice(request, account="Anonymous"):
    try:
        g = GeoIP2()
        ip = request.META.get("REMOTE_ADDR", None)


        local =  ['127.0.0.1', 'localhost', '0.0.0.0']

        if not ip:
            return None

        if ip in local:
            ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')



        instance = Device.objects.all().filter(ip=ip).first()

        if instance:
            return instance


        country_metadata = g.country(ip)
        country = country_metadata.get("country_name")
        city_metadata = g.city(ip)
        city = city_metadata.get("city")
        is_mobile = request.user_agent.is_mobile
        is_tablet = request.user_agent.is_tablet
        is_touch_capable = request.user_agent.is_touch_capable
        is_pc = request.user_agent.is_pc
        is_bot = request.user_agent.is_bot
        browser = request.user_agent.browser.family
        browser_version = request.user_agent.browser.version_string
        os = request.user_agent.os.family
        os_version = request.user_agent.os.version
        device = request.user_agent.device.family
        account = account

        instance = Device(
            ip=ip,
            country_metadata=country_metadata,
            country=country,
            city=city,
            city_metadata=city_metadata,
            is_mobile=is_mobile,
            is_tablet=is_tablet,
            is_touch_capable=is_touch_capable,
            is_pc=is_pc,
            is_bot=is_bot,
            browser=browser,
            browser_version=browser_version,
            os=os,
            os_version=os_version,
            device=device,
            account=account
        )

        instance.save()

        return instance

    except Exception:
        return None





@api_view(['POST'])
@permission_classes([AllowAny])
def logEvent(request: Request):
    try:
        
        event = request.data


        acc = request.user.username

        event['account'] = acc

        serializer = EventSerializer(data=event)


        if serializer.is_valid():
            event['device'] = getDevice(request, account=acc)
            serializer.create(event)


            if event.get("event_type") == "view-hashtag-posts":
                inst = Hashtag.objects.all().filter(hashtag=event.get("data")['hashtag']).first()

                if inst:
                    now = timezone.now()

                    if inst.created_at+timezone.timedelta(days=30) < now and inst.updated_at+timezone.timedelta(hours=1) < now:
                        # if the Hashtag was created longer than 30 days ago and updated longer than an hour ago then reset it's rank (only the yound and brave survive)
                        inst.rank=0
                        inst.save()
                    else:
                        if inst.updated_at+timezone.timedelta(minutes=10) > now:
                            # if the Hashtag was updated in the last 10 minutes then increment the rank plus a 100
                            inst.rank+=1
                            # hot af rn
                            inst.save() 

                        elif inst.updated_at+timezone.timedelta(hours=1) > now:
                            # if the Hashtag was updated in the last hour then increment the rank
                            inst.rank+=1
                            # picking up steam
                            inst.save()


                        elif inst.updated_at+timezone.timedelta(hours=4) < now:
                            # if this hashtag's rank was updated in the last 4 hours or more
                            # then decrement the rank (because it's falling off)
                            inst.rank-=1
                            # loosing steam
                            inst.save()

                        elif inst.updated_at+timezone.timedelta(days=1) < now:
                            # if the hashtag was last updated 1 day ago then reset it's rank
                            inst.rank=0
                            inst.save()


                        elif inst.updated_at+timezone.timedelta(days=2) <= now:

                            # it's dead
                            inst.rank=0
                            inst.save()



            if event.get("event_type") == "view-symbol-posts":
                inst = Symbol.objects.all().filter(symbol=event.get("data")['symbol']).first()
                if inst:

                    now = timezone.now()

                    if inst.created_at+timezone.timedelta(days=30) < now and inst.updated_at+timezone.timedelta(hours=1) < now:
                        # if the symbol was created longer than 30 days ago and updated longer than an hour ago then reset it's rank (only the yound and brave survive)
                        inst.rank=0
                        inst.save()
                    else:

                        if inst.updated_at+timezone.timedelta(minutes=10) > now:
                            # if the symbol was updated in the last 10 minutes then increment the rank plus a 100
                            inst.rank+=1
                            # hot af rn
                            inst.save() 

                        elif inst.updated_at+timezone.timedelta(hours=1) > now:
                            # if the Symbol was updated in the last hour then increment the rank
                            inst.rank+=1
                            # picking up steam
                            inst.save()


                        elif inst.updated_at+timezone.timedelta(hours=4) < now:
                            # if this symbol's rank was updated in the last 4 hours or more
                            # then decrement the rank (because it's falling off)
                            inst.rank-=1
                            # loosing steam
                            inst.save()


                        elif inst.updated_at+timezone.timedelta(days=1) < now:
                            # if the hashtag was last updated 1 day ago then reset it's rank
                            inst.rank=0
                            inst.save()


                        elif inst.updated_at+timezone.timedelta(days=2) <= now:

                            # it's dead
                            inst.rank=0
                            inst.save()

            return Response(status=200)



        return Response(status=400)

    except Exception:
        return Response(status=400)




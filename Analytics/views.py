from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from django.utils import timezone
from django.contrib.gis.geoip2 import GeoIP2
from voidbackApi.models.Post import Hashtag, Symbol
from .serializers import EventSerializer
from .models import Device
import urllib.request


def getip(request):
    try:
        ip = request.META.get('HTTP_X_FORWARDED_FOR')
        if ip:
            ip = ip.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    except Exception:
        return None


def getDevice(request, account="Anonymous"):
    try:
        g = GeoIP2()
        ip = getip(request)


        local =  ['127.0.0.1', 'localhost', '0.0.0.0']

        if not ip:
            return None

        if ip in local: # for local dev
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

        event['device'] = getDevice(request, account=acc)

        serializer = EventSerializer(data=event)


        if serializer.is_valid():
            serializer.create(event)


            if event.get("event_type") == "view-hashtag-posts":
                inst = Hashtag.objects.all().filter(hashtag=event.get("data")['hashtag']).first()

                if inst:
                    now = timezone.now()


                    if inst.updated_at+timezone.timedelta(hours=24) <= now:
                        # if the hashtag was last updated day or more ago then reset it's rank
                        inst.rank=0
                        inst.save()

                    else:
                        inst.rank+=1
                        inst.save()



            if event.get("event_type") == "view-symbol-posts":
                inst = Symbol.objects.all().filter(symbol=event.get("data")['symbol']).first()
                if inst:

                    now = timezone.now()

                    if inst.updated_at+timezone.timedelta(hours=24) <= now:
                        # if the hashtag was last updated day or more ago then reset it's rank
                        inst.rank=0
                        inst.save()

                    else:
                        inst.rank+=1
                        inst.save()


            return Response(status=200)


        return Response(status=400)

    except Exception:
        return Response(status=400)




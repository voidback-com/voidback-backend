from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response
from ..models.Platform import PlatformMessage, PlatformMessageImpression
from ..serializers import PlatformMessageSerializer




@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getPlatformMessage(request: Request):
    try:

        instance = PlatformMessage.objects.all().last()

        if not instance:
            return Response(status=204)


        last_imp = PlatformMessageImpression.objects.all().filter(account=request.user.id).last()

        if last_imp and last_imp.message==instance:
            return Response(status=204) # no new message

        else:
            imp = PlatformMessageImpression(message=instance, account=request.user)
            imp.save()

            serializer = PlatformMessageSerializer(instance)

            return Response(serializer.data, status=200)

    except Exception:
        return Response(data={"error": "Error fetching platform message!"}, status=400)





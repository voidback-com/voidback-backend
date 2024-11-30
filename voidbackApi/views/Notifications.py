from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response
from ..models.Notifications import Notification
from ..serializers import NotificationSerializer




@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getNotifications(request: Request):
    try:

        skip = request.query_params.get("skip")
        limit = request.query_params.get("limit")

        instance = Notification.objects.all().filter(account=request.user.username).order_by("-created_at")[int(skip):int(limit)]

        serializer = NotificationSerializer(instance, many=True)

        return Response(serializer.data, status=200)


    except Exception:
        return Response(data={"error": "Error fetching notifications!"}, status=400)





@api_view(["GET"])
@permission_classes([IsAuthenticated])
def readNotification(request: Request):
    try:
        instances = Notification.objects.all().filter(account=request.user)

        for instance in instances:
            instance.isRead = True
            instance.save()

        return Response(status=200)
    except Exception:
        return Response(data={"error": "Error updating the notification status!"}, status=400)




@api_view(["GET"])
@permission_classes([IsAuthenticated])
def deleteNotification(request: Request, pk: int):
    try:
        instance = Notification.objects.all().filter(pk=pk).first()

        if instance:
            instance.delete()

        return Response(status=200)
    except Exception:
        return Response(data={"error": "Error deleting notification!"}, status=400)





 

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def deleteAllNotification(request: Request):
    try:
        instances = Notification.objects.all().filter(account=request.user)

        for i in instances:
            i.delete()

        return Response(status=200)
    except Exception:
        return Response(data={"error": "Error deleting notification!"}, status=400)


from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from ..pagination.defaultPagination import DefaultSetPagination
from ..serializers.Inbox import InboxMessageSerializer, InboxMessage
from ..models.Post import Post
from ..models.Account import Account
from ..models.Notifications import newNotification

import json




# send an inbox message
class CreateInboxMessage(APIView):
    permission_classes = [IsAuthenticated]


    def post(self, request: Request):
        try:
            data = request.data

            data['from_account'] = request.user


            data['to_account'] = Account.objects.all().filter(username=request.data['to_account']).first()


            serializer = InboxMessageSerializer(data=data)


            if serializer.is_valid():
                data['post'] = Post.objects.all().filter(pk=request.data['post']).first()

                serializer.create(data)

                newNotification(data["to_account"], request.user.full_name, "/inbox", fromAvatar=request.user.avatar, avatarVerified=request.user.isVerified, fromNameMessage=f"New inbox message from", icon="inbox")
                return Response(data={"status": "success"}, status=200)

            return Response(data=serializer.errors, status=400)

        except Exception:
            return Response(data={"error": "something went wrong, please try again!"}, status=400)

 


class InboxMessagesView(ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = [DefaultSetPagination]
    serializer_class = InboxMessageSerializer
    pagination_class = DefaultSetPagination


    def get_queryset(self):
        return InboxMessage.objects.all().filter(to_account=self.request.user.username).order_by("-created_at")





@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def deleteInboxMessage(request: Request, message_id: int):
    try:
        instance = InboxMessage.objects.all().filter(pk=message_id).first()

        if instance.from_account == request.user or instance.to_account == request.user:
            instance.delete()

            return Response(data={"message": "success"}, status=200)

        return Response(data={"Error": "This inbox message does not exist or wasn't sent to your inbox."}, status=400)

    except Exception:
        return Response(data={"error": "something went wrong deleting this inbox message, please try again!"}, status=400)






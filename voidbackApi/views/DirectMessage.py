from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from voidbackApi.models.Account import AccountActiveStatus
from voidbackApi.pagination.defaultPagination import DefaultSetPagination
from django.db.models import Q
from ..serializers.DirectMessage import (
    DMMessageSerializer,
    DirectMessageSession, 
    DMMessage,
    DirectMessageSessionSerializer
)
from ..serializers.Account import Account
import json




# create a dm session
class CreateDMSession(APIView):
    permission_classes = [IsAuthenticated]


    def post(self, request: Request):
        try:
            data = request.data

            data["initiator"] = request.user
            data['friend'] = Account.objects.all().filter(username=data['friend']).first()

            if not data['friend']:
                return Response(data={"error": "This account does not exist!"}, status=400)

            isFollowing = Follow.objects.all().filter(following=data['initator'], follower=data['friend']).first()

            if not isFollowing:
                return Response(data={"error": "This account does not follow you!"}, status=400)

            serializer = DirectMessageSessionSerializer(data=data)

            if serializer.is_valid():
                serializer.create(data)

                return Response(serializer.data, status=200)

        except Exception:
            return Response(data={"error": "something went wrong, please try again!"}, status=400)



# delete a dm session
class DeleteDMSession(APIView):
    permission_classes = [IsAuthenticated]


    def delete(self, request: Request):
        try:
            data = request.data

            session = data.get("session")

            sess = DirectMessageSession.objects.all().filter(pk=session)


            if sess:
                if request.user!=sess.initiator and request.user!=sess.friend:
                    return Response(data={"error": "This dm session does not exist!"}, status=400)
                else:
                    sess.delete()
                    return Response(data={"data": None}, status=200)
            else:
                return Response(data={"data": None}, status=200)

        except Exception:
            return Response(data={"error": "something went wrong, please try again!"}, status=400)



class SendDirectMessage(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request):
        try:
            # only notify those who haven't archived the session
            data = json.loads(request.data.get("data", {}))


            image = request.FILES.get("image")

            if image:
                data['image'] = image


            data['sender'] = request.user


            serializer = DMMessageSerializer(data=data)

            if serializer.is_valid():
                r = serializer.create(data)


                return Response(DMMessageSerializer(r).data, status=200)

            else:
                print(serializer.errors)
                return Response(serializer.errors, status=400)

        except KeyboardInterrupt:
            return Response(data={"error": "something went wrong, please try again!"}, status=400)




class DeleteDirectMessage(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request: Request):
        try:
            data = request.data

            # message pk
            message = data.get("message")

            instance = DMMessage.objects.all().filter(pk=message).first()


            if instance and instance.sender.username == request.user.username:
                instance.delete()

            return Response(data={"data": None}, status=200)

        except KeyboardInterrupt:
            return Response(data={"error": "something went wrong, please try again!"}, status=400)





@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getSessions(request: Request):
    try:
        # latest messages from distinct sessions excluding archived sessions
        sessions = DirectMessageSession.objects.all().filter(Q(friend=request.user) | Q(initiator=request.user)).distinct("id")

        

        latestMessages = DMMessage.objects.all().filter(session__in=sessions).exclude(session__archived_by__in=[request.user]).order_by("session_id", "-sent_at").distinct("session")


        serialized = DMMessageSerializer(latestMessages, many=True)

        return Response(serialized.data, status=200)

    except Exception:
        return Response(data={"error": "something went wrong, please try again!"}, status=400)





@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getArchivedSessions(request: Request):
    try:
        # latest messages from distinct archived sessions
        latestMessages = DMMessage.objects.all().filter(Q(sender=request.user) | Q(session__friend=request.user) | Q(session__initiator=request.user), session_archived_by__in=[request.user]).exclude(session__archived_by__in=[request.user]).order_by("-sent_at").order_by("seen").order_by("-seen_at").order_by("session__id").distinct("session__id")
        serialized = DMMessageSerializer(latestMessages, many=True)

        return Response(serialized.data, status=200)

    except Exception:
        return Response(data={"error": "something went wrong, please try again!"}, status=400)





@api_view(["POST"])
@permission_classes([IsAuthenticated])
def archiveSession(request: Request):
    try:
        session = request.data.get("session")

        session = DirectMessageSession.objects.all().filter(pk=session).exclude(archived_by__in=[request.user]).first()

        if not session:
            return Response(status=200)

        else:
            session.archived_by.add(request.user)
            session.save()

        return Response(status=200)

    except Exception:
        return Response(status=200)





@api_view(["POST"])
@permission_classes([IsAuthenticated])
def unarchiveSession(request: Request):
    try:
        session = request.data.get("session")

        session = DirectMessageSession.objects.all().filter(pk=session, archived_by__in=[request.user]).first()

        if not session:
            return Response(status=200)

        else:
            session.archived_by.remove(request.user)
            session.save()

        return Response(status=200)

    except Exception:
        return Response(status=200)



 
class DirectMessageSessionView(ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = [DefaultSetPagination]
    serializer_class = DMMessageSerializer
    pagination_class = DefaultSetPagination


    def get_queryset(self):
        session = self.request.query_params.get("session")

        sess = DirectMessageSession.objects.all().filter(pk=session).first()

        if sess:

            if sess.initiator!=self.request.user and sess.friend!=self.request.user:
                return []

            messages = DMMessage.objects.all().filter(session=sess).order_by("-sent_at")

            status = AccountActiveStatus.objects.all().filter(account=self.request.user).first()

            if status:
                status.save()

            for message in messages:
                if not message.seen and message.sender!=self.request.user:
                    message.seen = True
                    message.save()

            return messages

        else:
            return []





from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from ..serializers.DirectMessage import (
    DirectMessageSession, 
    DMMessage,
    DirectMessageSessionSerializer
)
from ..serializers.Account import Account
from ..models.Notifications import newNotification
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

            serializer = DirectMessageSessionSerializer(data=data)

            if serializer.is_valid():
                serializer.create(data)

                return Response(serializer.data, status=200)

        except Exception:
            return Response(data={"error": "something went wrong, please try again!"}, status=400)




@permission_classes([IsAuthenticated])
@api_view(["GET"])
def getSessions(request: Request):
    try:
        pass
    except Exception:
        pass

 






# createSession() initiator can only create a session with someone who follows them back

# GetSessions() order by the latest chate sent/recieved etc...

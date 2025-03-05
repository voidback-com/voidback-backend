from itertools import chain
from django.db.models.query import Q
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import CreateAPIView, ListAPIView, ListCreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.views import Response

from voidbackApi.models.EdgeRoom import MemberPermissions
from voidbackApi.models.Post import Post
from voidbackApi.pagination.defaultPagination import DefaultSetPagination
from voidbackApi.permissions.roomMemberPermissions import IsRoomMember
from ..serializers.Post import PostSerializer
from ..serializers.EdgeRoom import (
    EdgeRoom,
    EdgeRoomConfig,
    EdgeRoomSerializer,
    MemberPermissionsSerializer,
    RoomMembershipSerializer,
    RoomMembership
)






# create an edge room
class CreateEdgeRoomView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EdgeRoomSerializer
    permission_classes = [IsAuthenticated]

# Make sure to create an edgeMember for the admin 


# List edge rooms am a member of
class ListMyEdgeRoomsView(ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = DefaultSetPagination
    serializer_class = EdgeRoomSerializer


    def get_queryset(self):
        try:
            instance = RoomMembership.objects.all().filter(account=self.request.user).order_by("-room__rank").values("room")


            insts = EdgeRoom.objects.all().filter(Q(config__admin=self.request.user) | Q(pk__in=instance)).order_by("-rank")

            return insts
        except Exception:
            return []




# List edge rooms am an admin of 
class ListMyEdgeRoomsAdminView(ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = DefaultSetPagination
    serializer_class = EdgeRoomSerializer


    def get_queryset(self):
        try:
            instance = EdgeRoom.objects.all().filter(config__admin=self.request.user).order_by("-rank")
            return instance
        except Exception:
            return []



# returns all the posts in the edge room
class ListRoomPostsView(ListAPIView):
    permission_classes = [IsRoomMember]
    pagination_class = DefaultSetPagination
    serializer_class = PostSerializer


    def get_queryset(self):
        try:
            room = self.request.query_params.get("room")
            instance = Post.objects.all().filter(room__name=room, parent_post=None).order_by("-created_at", "-rank")
            return instance
        except Exception:
            return []





@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getMembership(request: Request):
    try:

        room = request.query_params.get("room")

        instance = RoomMembership.objects.all().filter(account=request.user, room__name=room).first()

        serializer = RoomMembershipSerializer(instance)

        return Response(serializer.data, status=200)

    except Exception:
        return Response({"error": "Failed to fetch your room mebership."}, status=400)





@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getTopRankingRooms(request: Request):
    try:
        rooms = EdgeRoom.objects.all().order_by("-rank")[0:20]


        data = []

        for room in rooms:
            serialized = EdgeRoomSerializer(room)
            members = RoomMembership.objects.all().filter(room=room).count()
            res = {"room": serialized.data, "members": members}
            data.append(res)


        return Response(data, status=200)

    except Exception:
        return Response(data={"error": f"Error fetching top ranking rooms!"}, status=400)




@api_view(["POST"])
@permission_classes([IsAuthenticated])
def joinEdgeRoom(request: Request):
    try:

        data = request.data

        serializer = RoomMembershipSerializer(data=data)

        if serializer.is_valid():
            serializer.create(data)

            return Response(serializer.data, status=200)

        return Response({"error": "Failed to join room."}, status=400)

    except Exception:
        return Response({"error": "Failed to join room."}, status=400)




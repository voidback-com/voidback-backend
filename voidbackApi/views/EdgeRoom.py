from rest_framework.generics import CreateAPIView, ListAPIView, ListCreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from voidbackApi.pagination.defaultPagination import DefaultSetPagination
from ..serializers.EdgeRoom import (
    EdgeRoom,
    EdgeRoomConfig,
    EdgeRoomSerializer,
    RoomMembershipSerializer,
    RoomMembership
)




# create an edge room
class CreateEdgeRoomView(CreateAPIView):
    serializer_class = EdgeRoomSerializer
    permission_classes = [IsAuthenticated]



# List edge rooms am a member of
class ListMyEdgeRoomsView(ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = DefaultSetPagination
    serializer_class = EdgeRoomSerializer


    def get_queryset(self):
        try:
            instance = RoomMembership.objects.all().filter(account=self.request.user).values("room").order("-rank")
            return instance
        except Exception:
            return []




# List edge rooms am an admin of 
class ListMyEdgeRoomsAdminView(ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = DefaultSetPagination
    serializer_class = EdgeRoomSerializer


    def get_queryset(self):
        try:
            instance = EdgeRoom.objects.all().filter(config__admin=self.request.user).order("-rank")
            return instance
        except Exception:
            return []




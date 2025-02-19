from rest_framework.serializers import BooleanField, ImageField, IntegerField, ListField, ModelSerializer, FileField, SerializerMethodField
from ..models import (
    RoomCategory,
    EdgeRoomConfig,
    EdgeRoom,
    MemberPermissions,
    RoomMembership
)
from .Account import PublicAccountSerializer


class RoomCategorySerializer(ModelSerializer):

    class Meta:
        model = RoomCategory

        fields = "__all__"




class EdgeRoomConfigSerializer(ModelSerializer):
    admin = PublicAccountSerializer(read_only=True)

    class Meta:
        model = EdgeRoomConfig

        fields = "__all__"


    

class EdgeRoomSerializer(ModelSerializer):

    categories = RoomCategorySerializer(many=True)
    config = EdgeRoomConfigSerializer()



    class Meta:
        model = EdgeRoom

        fields = "__all__"



class MemberPermissionsSerializer(ModelSerializer):

    updated_by = PublicAccountSerializer(read_only=True)

    class Meta:
        model = MemberPermissions

        fields = "__all__"



class RoomMembershipSerializer(ModelSerializer):

    room = EdgeRoomSerializer(read_only=True)
    permissions = MemberPermissionsSerializer(read_only=True)
    account = PublicAccountSerializer(read_only=True)

    class Meta:
        model = RoomMembership

        fields = "__all__"




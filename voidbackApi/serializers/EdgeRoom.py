from rest_framework.serializers import ModelSerializer
from ..models import (
    RoomCategory,
    EdgeRoomConfig,
    EdgeRoom,
    MemberPermissions,
    RoomMembership
)
from .Account import PublicAccountSerializer, Account



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


    def create(self, validated_data):

        config = validated_data.pop("config")

        conf = EdgeRoomConfig(**config)

        conf.save()

        validated_data['config'] = conf

        categories = validated_data.pop("categories")

        c_instances = []

        for i in categories:
            c = RoomCategory.objects.all().filter(category=i['category']).first() 
            if c:
                c.rank+=1
                c.save()
                c_instances.append(c.pk)

            else:
                c = RoomCategory(category=i['category'])
                c.rank+=1
                c.save()
                c_instances.append(c.pk)



        instance = EdgeRoom(**validated_data)

        instance.save()

        instance.categories.set(c_instances)

        instance.save()



        return instance


class MemberPermissionsSerializer(ModelSerializer):

    updated_by = PublicAccountSerializer(read_only=True)

    class Meta:
        model = MemberPermissions

        fields = "__all__"




class RoomMembershipSerializer(ModelSerializer):

    room = EdgeRoomSerializer(read_only=True)
    permissions = MemberPermissionsSerializer()
    account = PublicAccountSerializer(read_only=True)

    class Meta:
        model = RoomMembership

        fields = "__all__"


    def create(self, validated_data):

        permissions = validated_data.pop('permissions')

        room = validated_data.pop("room")
        acc = validated_data.pop("account")

        account_inst = Account.objects.all().filter(pk=acc).first()

        rm_inst = EdgeRoom.objects.all().filter(pk=room).first()

        rm_inst.rank+=1
        rm_inst.save()

        validated_data['room'] = rm_inst
        validated_data['account'] = account_inst




        perm = MemberPermissions(**permissions)

        perm.save()


        validated_data['permissions'] = perm

        instance = RoomMembership(**validated_data)

        instance.save()


        return instance



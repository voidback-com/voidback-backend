from rest_framework.serializers import ModelSerializer
from .models import Device, Event




class DeviceSerializer(ModelSerializer):

    class Meta:

        model = Device

        fields = "__all__"



class EventSerializer(ModelSerializer):
    device = DeviceSerializer(read_only=True)

    class Meta:

        model = Event

        fields = "__all__"



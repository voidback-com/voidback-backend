from rest_framework.serializers import ModelSerializer
from .models import Device, Event




class EventSerializer(ModelSerializer):

    class Meta:

        model = Event

        fields = "__all__"



class DeviceSerializer(ModelSerializer):

    class Meta:

        model = Device

        fields = "__all__"

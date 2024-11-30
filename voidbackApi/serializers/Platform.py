from rest_framework.serializers import ModelSerializer

from ..models.Platform import *


class PlatformMessageSerializer(ModelSerializer):

    class Meta:
        model = PlatformMessage

        fields = ["image", "title", "description", "created_at", "links"]




from rest_framework.serializers import BooleanField, ImageField, IntegerField, ListField, ModelSerializer, FileField, SerializerMethodField
from voidbackApi.serializers.Post import PostSerializer
from ..models import (
    DMImage,
    DMVoiceNote,
    DirectMessageSession,
    DMMessage
)
from .Account import AccountSerializer


class DMImageSerializer(ModelSerializer):
    image = ImageField()

    class Meta:
        model = DMImage

        fields = ["image"]



class DMVoiceNoteSerializer(ModelSerializer):
    voiceNote = FileField()

    class Meta:
        model = DMVoiceNote

        fields = ['voiceNote']




class DirectMessageSessionSerializer(ModelSerializer):
    initiator = AccountSerializer(read_only=True)
    friend = AccountSerializer()

    class Meta:
        model = DirectMessageSession

        fields = "__all__"




class DMMessageSerializer(ModelSerializer):
    session = DirectMessageSession()
    sender = AccountSerializer()
    post = PostSerializer()

    image = DMImageSerializer()
    voiceNote = DMVoiceNoteSerializer()
    parent = SerializerMethodField(read_only=True)

    class Meta:
        model = DMMessage

        fields = "__all__"



    def get_parent(self, obj):
        if type(obj) == dict:
            if 'parent' in obj:
                if obj['parent'] is not None:
                    return DMMessageSerializer(obj['parent']).data
                else:
                    return None
        else:
            if obj.parent is not None:
                return DMMessageSerializer(obj.parent_post).data
            else:
                return None



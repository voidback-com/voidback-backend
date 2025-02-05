from rest_framework.serializers import BooleanField, ImageField, IntegerField, ListField, ModelSerializer, FileField, SerializerMethodField
from voidbackApi.serializers.Post import PostSerializer
from ..models import (
    DMImage,
    DirectMessageSession,
    DMMessage,
    Post,
)
from .Account import AccountSerializer


class DMImageSerializer(ModelSerializer):
    image = ImageField()

    class Meta:
        model = DMImage

        fields = ["image"]




class DirectMessageSessionSerializer(ModelSerializer):
    initiator = AccountSerializer(read_only=True)
    friend = AccountSerializer(read_only=True)
    archived_by = AccountSerializer(read_only=True, many=True)

    class Meta:
        model = DirectMessageSession

        fields = "__all__"




class DMMessageSerializer(ModelSerializer):
    session = DirectMessageSessionSerializer(read_only=True)
    sender = AccountSerializer(read_only=True)
    post = PostSerializer(read_only=True)

    image = DMImageSerializer(read_only=True)

    class Meta:
        model = DMMessage

        fields = "__all__"



    def create(self, validated_data):
        image = None
        if "image" in validated_data:
            image = validated_data.pop("image")
            image = DMImage(image=image)
            image.save()


        session = None
        if "session" in validated_data:
            session = validated_data.pop("session")
            session = DirectMessageSession.objects.all().filter(pk=session).first()

        post = None
        if "post" in validated_data:
            post = validated_data.pop("post")
            post = Post.objects.all().filter(pk=post).first()


        instance = DMMessage(**validated_data)

        instance.image = image
        instance.session = session
        instance.post = post

        instance.save()

        return instance





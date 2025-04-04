from rest_framework import serializers
from rest_framework.serializers import BooleanField, ImageField, IntegerField, ListField, ModelSerializer, ReturnDict, SerializerMethodField
from voidbackApi.models import Writeup
from voidbackApi.models.Writeup import WriteUpImpression
from .Account import PublicAccountSerializer, Account
from ..models import (
    Tag,
    ForYou,
    WriteUp,
    Series,
    WriteUpThumbnail,
    WriteUpImpression,
    Comment,
    CommentImpression
)





class TagSerializer(ModelSerializer):

    class Meta:
        model = Tag

        fields = ["id", "tag", "rank"]





class WriteUpThumbnailSerializer(ModelSerializer):
    thumbnail = ImageField()

    class Meta:
        model = WriteUpThumbnail
        fields = ["thumbnail"]



class SeriesSerializer(ModelSerializer):

    author = PublicAccountSerializer(read_only=True)

    class Meta:
        model = Series
        fields = "__all__"



class WriteUpSerializer(ModelSerializer):

    tags = TagSerializer(many=True, read_only=True)

    thumbnail = WriteUpThumbnailSerializer(read_only=True)

    author = PublicAccountSerializer(read_only=True)

    series = SeriesSerializer(read_only=True)


    class Meta:
        model = WriteUp
        fields = "__all__"


    def create(self, validated_data):
        tags = validated_data.pop("tags")
        thumbnail = validated_data.pop("thumbnail")

        ti = WriteUpThumbnail(thumbnail=thumbnail)
        ti.save()

        validated_data['thumbnail'] = ti


        instance = WriteUp(**validated_data)

        instance.save()


        for tag in tags:
            hinstance = Tag.objects.all().filter(tag=tag['tag']).first()

            if not hinstance:
                hinstance = Tag(**tag)
                hinstance.rank = 1
                hinstance.save()

            else:
                hinstance.rank += 1
                hinstance.save()


            instance.tags.add(hinstance)

        instance.save()

        return instance



class WriteUpImpressionSerializer(ModelSerializer):

    class Meta:
        model = WriteUpImpression

        fields = "__all__"


    def create(self, validated_data):
        writeup = validated_data.pop("writeup")

        p = WriteUp.objects.all().filter(pk=writeup).first()

        instance = WriteUpImpression(writeup=p, **validated_data)

        instance.save()

        return instance




class CommentSerializer(ModelSerializer):
    parent = serializers.SerializerMethodField(read_only=True, method_name="get_parent_comment")
    author = PublicAccountSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = "__all__"


    def create(self, validated_data):
        validated_data['writeup'] = WriteUp.objects.all().filter(pk=validated_data['writeup']).first()

        inst = Comment(**validated_data)
        inst.save()

        return inst


    def get_parent_comment(self, obj):
        if type(obj) == dict:
            if 'parent' in obj:
                if obj['parent'] is not None:
                    return CommentSerializer(instance=obj).data
                else:
                    return None

        else:
            if obj.parent is not None:
                return CommentSerializer(obj.parent).data

            else:
                return None



class CommentImpressionSerializer(ModelSerializer):

    class Meta:
        model = CommentImpression

        fields = "__all__"


    def create(self, validated_data):
        comment = validated_data.pop("comment")

        p = Comment.objects.all().filter(pk=comment).first()

        instance = CommentImpression(comment=p, **validated_data)

        instance.save()

        return instance



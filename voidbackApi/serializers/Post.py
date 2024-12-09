from rest_framework.serializers import BooleanField, ImageField, IntegerField, ListField, ModelSerializer, ReturnDict, SerializerMethodField
from .Account import PublicAccountSerializer, Account
from ..models import (
    Hashtag,
    Symbol,
    PostImage,
    Post,
    PostImpression,
    PostMetadata,
    ForYou
)





class HashtagSerializer(ModelSerializer):

    class Meta:
        model = Hashtag

        fields = ["id", "hashtag"]




class SymbolSerializer(ModelSerializer):

    class Meta:
        model = Symbol

        fields = ["id", "symbol"]





class PostImageSerializer(ModelSerializer):
    image = ImageField()

    class Meta:
        model = PostImage

        fields = ["image"]



class PostSerializer(ModelSerializer):

    hashtags = HashtagSerializer(many=True, read_only=True)
    symbols = SymbolSerializer(many=True, read_only=True)
    mentions = PublicAccountSerializer(many=True, read_only=True)

    image = PostImageSerializer(read_only=True)

    author = PublicAccountSerializer(read_only=True)

    parent_post = SerializerMethodField(read_only=True)


    class Meta:
        model = Post
        fields = "__all__"
        read_only_fields = ['created_at', "rank", "updated_at"]


    def get_parent_post(self, obj):
        if type(obj) == dict:
            if 'parent_post' in obj:
                if obj['parent_post'] is not None:
                    return PostSerializer(obj['parent_post']).data
                else:
                    return None
        else:
            if obj.parent_post is not None:
                return PostSerializer(obj.parent_post).data
            else:
                return None



    def create(self, validated_data):
        hashtags = validated_data.pop("hashtags")
        symbols = validated_data.pop("symbols")
        mentions = validated_data.pop("mentions")
        image = validated_data.pop("image")


        instance = Post(**validated_data)


        instance.save()


        for hashtag in hashtags:
            hinstance = Hashtag.objects.all().filter(hashtag=hashtag['hashtag']).first()

            if not hinstance:
                hinstance = Hashtag(**hashtag)
                hinstance.save()
            instance.hashtags.add(hinstance)


        for symbol in symbols:
            sinstance = Symbol.objects.all().filter(symbol=symbol['symbol']).first()

            if not sinstance:
                sinstance = Symbol(**symbol)
                sinstance.save()
            instance.symbols.add(sinstance)


        for mention in mentions:
            minstance = Account.objects.all().filter(username=mention['username']).first()

            if not minstance:
                continue

            instance.mentions.add(minstance)


        if image:
            iinstance = PostImage(image=image)
            iinstance.save()

            instance.image = iinstance


        instance.save()

        return instance



class PostImpressionSerializer(ModelSerializer):

    class Meta:
        model = PostImpression

        fields = "__all__"


    def create(self, validated_data):
        post = validated_data.pop("post")

        p = Post.objects.all().filter(pk=post).first()

        instance = PostImpression(post=p, **validated_data)

        instance.save()

        return instance




class PostMetadataSerializer(ModelSerializer):
    post = PostSerializer(read_only=True)

    class Meta:
        model = PostMetadata

        fields = "__all__"


    def create(self, validated_data):
        post = validated_data.pop("post")

        p = Post.objects.all().filter(pk=post).first()

        instance = PostMetadata(post=p, **validated_data)

        instance.save()

        return instance




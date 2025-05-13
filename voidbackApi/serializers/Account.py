from rest_framework.serializers import BooleanField, DateTimeField, IntegerField, ModelSerializer, FileField, CharField
from ..models import Account, Follow



class AccountSerializer(ModelSerializer):
    password = CharField(write_only=True)
    rank = IntegerField(read_only=True)
    is_staff = BooleanField(read_only=True)
    email_verified = BooleanField(read_only=True)

    class Meta:
        model = Account

        fields = ["email", "full_name", "username", "avatar", "bio", "site_link", "rank", "password", "is_staff", "isVerified", "email_verified", "id"]


    def create(self, validated_data):
        instance = Account(**validated_data)
        instance.set_password(validated_data['password'])
        instance.save()
        return instance


    def update(self, instance, validated_data):
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
        
        for i in validated_data:
            if i=="email":
                instance.email = validated_data.get("email")

            elif i=="full_name":
                instance.full_name = validated_data.get("full_name")

            elif i=="bio":
                instance.bio = validated_data.get("bio")

            elif i=="site_link":
                instance.site_link = validated_data.get("site_link")

            elif i=="avatar":
                instance.avatar = validated_data.get("avatar")


        instance.save()
        return instance



class PublicAccountSerializer(ModelSerializer):

    class Meta:
        model = Account
        fields = ["full_name", "username", "avatar", "bio", "site_link", "isVerified", "rank"]




class FollowSerializer(ModelSerializer):
    follower = PublicAccountSerializer(read_only=True)
    following = PublicAccountSerializer(read_only=True)

    class Meta:
        model = Follow

        fields = "__all__"






from rest_framework.serializers import BooleanField, ImageField, IntegerField, ListField, ModelSerializer
from ..models import (
    InboxMessage,
)
from .Account import PublicAccountSerializer
from .Post import PostSerializer


class InboxMessageSerializer(ModelSerializer):
    from_account = PublicAccountSerializer(read_only=True)
    post = PostSerializer(read_only=True)

    class Meta:
        model = InboxMessage

        fields = "__all__"



from rest_framework.serializers import ModelSerializer
from .Account import AccountSerializer
from ..models.Notifications import Notification
from .Post import PostSerializer


class NotificationSerializer(ModelSerializer):
    account = AccountSerializer(read_only=True)
    post = PostSerializer(read_only=True)

    class Meta:
        model = Notification

        fields = "__all__"



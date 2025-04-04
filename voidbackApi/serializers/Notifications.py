from rest_framework.serializers import ModelSerializer
from .Account import AccountSerializer
from ..models.Notifications import Notification


class NotificationSerializer(ModelSerializer):
    account = AccountSerializer(read_only=True)

    class Meta:
        model = Notification

        fields = "__all__"



from rest_framework.serializers import BooleanField, ImageField, IntegerField, ListField, ModelSerializer
from ..models import (
    DataHubQuery,
    DataHubAccount,
    DataHubPositionPoll,
    DataHubFeedbackPoll
)
from .Account import AccountSerializer


class DataHubAccountSerializer(ModelSerializer):

    account = AccountSerializer(read_only=True)
    queries_left = IntegerField()

    class Meta:
        model = DataHubAccount
        fields = "__all__"


class DataHubQuerySerializer(ModelSerializer):

    account = DataHubAccountSerializer(read_only=True)

    class Meta:
        model = DataHubQuery
        fields = "__all__"





class DataHubPositionPollSerializer(ModelSerializer):

    account = DataHubAccountSerializer(read_only=True)

    class Meta:
        model = DataHubPositionPoll
        fields = "__all__"




class DataHubFeedbackPollSerializer(ModelSerializer):

    account = DataHubAccountSerializer(read_only=True)

    class Meta:
        model = DataHubFeedbackPoll
        fields = "__all__"





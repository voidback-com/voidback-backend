from rest_framework.serializers import ModelSerializer
from ..models import (
    SearchQuery
)




class SearchQuerySerializer(ModelSerializer):

    class Meta:

        model = SearchQuery

        fields = "__all__"



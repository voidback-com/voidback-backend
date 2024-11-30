from rest_framework.serializers import BooleanField, ImageField, IntegerField, ListField, ModelSerializer
from ..models import (
    ResearchPaper,
    ResearchPaperImpression
)
from .Account import AccountSerializer



class ResearchPaperSerializer(ModelSerializer):
    author = AccountSerializer(read_only=True)


    class Meta:
        model = ResearchPaper

        fields = "__all__"



class ResearchPaperImpressionSerializer(ModelSerializer):
    account = AccountSerializer(read_only=True)
    paper = ResearchPaperSerializer(read_only=True)

    class Meta:
        model = ResearchPaperImpression

        fields = "__all__"



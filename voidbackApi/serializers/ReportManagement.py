from django.db import models
from rest_framework.serializers import ModelSerializer
from .Account import AccountSerializer
from ..models.ReportManagement import Report




# a user made report
class ReportSerializer(ModelSerializer):

    class Meta:
        model = Report
        fields = "__all__"



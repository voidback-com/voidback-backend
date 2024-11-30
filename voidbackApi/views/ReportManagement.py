from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from ..serializers.ReportManagement import ReportSerializer



class ReportView(CreateAPIView):
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated]




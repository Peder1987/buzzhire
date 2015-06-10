from django.db.models import Q
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import JobRequestSerializer, DriverJobRequestSerializer
from ..models import JobRequest, DriverJobRequest


class JobRequestViewSet(viewsets.ReadOnlyModelViewSet):
    "All job requests."
    serializer_class = JobRequestSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return JobRequest.objects.all()


class DriverJobRequestViewSet(viewsets.ReadOnlyModelViewSet):
    "All driver job requests."
    serializer_class = DriverJobRequestSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return DriverJobRequest.objects.all()

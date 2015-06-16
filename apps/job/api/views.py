from django.db.models import Q
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import JobRequestSerializer, DriverJobRequestSerializer
from ..models import JobRequest
from apps.service.driver.models import DriverJobRequest


class JobRequestViewSet(viewsets.ReadOnlyModelViewSet):
    "All job requests.  Publicly viewable information."
    serializer_class = JobRequestSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return JobRequest.objects.all()


class DriverJobRequestViewSet(viewsets.ReadOnlyModelViewSet):
    """All driver job requests.  Publicly viewable information.
    
    * `flexible_vehicle_type`: The flexible vehicle type that would
      be appropriate for the job, or null if any vehicle would be appropriate.
    """
    serializer_class = DriverJobRequestSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return DriverJobRequest.objects.all()

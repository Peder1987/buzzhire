from django.db.models import Q
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import JobRequestSerializer
from ..models import JobRequest


class JobRequestViewSet(viewsets.ReadOnlyModelViewSet):
    "All job requests.  Publicly viewable information."
    serializer_class = JobRequestSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return JobRequest.objects.all()


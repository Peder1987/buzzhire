from django.db.models import Q
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import JobRequestSerializer
from ..models import JobRequest


class JobRequestViewSet(viewsets.ReadOnlyModelViewSet):
    """All job requests.  Publicly viewable information.
    
    - `years_experience` The minimum number of years of working experience
       required. Integer.  Choices are:
        - `0` - Less than 1 year
        - `1` - 1 - 3 years
        - `3` - 3 - 5 years
        - `5` - More than 5 years
    """
    serializer_class = JobRequestSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return JobRequest.objects.all()


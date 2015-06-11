from django.db.models import Q
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import PublicFreelancerSerializer
from ..models import Freelancer


class PublicFreelancerViewSet(viewsets.ReadOnlyModelViewSet):
    "All published freelancers - publicly available information."
    serializer_class = PublicFreelancerSerializer

    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Freelancer.published_objects.all()

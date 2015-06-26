from rest_framework import viewsets
from ..freelancer.permissions import FreelancerOnlyPermission
from .serializers import ClientForFreelancerSerializer
from apps.client.models import Client


class ClientForFreelancerViewSet(viewsets.ReadOnlyModelViewSet):
    "Clients viewable by the currently logged in freelancer."
    serializer_class = ClientForFreelancerSerializer
    permission_classes = (FreelancerOnlyPermission,)

    def get_queryset(self):
        # TODO
        return Client.objects.all()


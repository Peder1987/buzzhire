from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import PublicClientSerializer
from ..models import Client


class PublicClientViewSet(viewsets.ReadOnlyModelViewSet):
    "All clients - publicly available information."
    serializer_class = PublicClientSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Client.objects.all()



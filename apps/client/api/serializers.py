from django.forms import widgets
from rest_framework import serializers
from ..models import Client


class PublicClientSerializer(serializers.ModelSerializer):
    """Serializer that exposes information on the client
    appropriate for public use.
    """
    class Meta:
        model = Client
        fields = ('id', 'reference_number', 'first_name', 'last_name')

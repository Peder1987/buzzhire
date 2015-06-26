from django.forms import widgets
from rest_framework import serializers
from apps.client.models import Client


class ClientForFreelancerSerializer(serializers.ModelSerializer):
    """Serializer that exposes information on the client
    appropriate for freelancer use.
    """
    class Meta:
        model = Client
        fields = ('id', 'reference_number', 'first_name', 'last_name')

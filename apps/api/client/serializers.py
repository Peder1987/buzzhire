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


class OwnClientSerializer(ClientForFreelancerSerializer):
    """Serializer that exposes information on the client
    profile for their own use.
    """

    email = serializers.SerializerMethodField()
    def get_email(self, obj):
        return obj.user.email


    class Meta(ClientForFreelancerSerializer.Meta):
        fields = ClientForFreelancerSerializer.Meta.fields + (
                'email', 'mobile', 'company_name')

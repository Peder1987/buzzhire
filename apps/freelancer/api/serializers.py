from django.forms import widgets
from rest_framework import serializers
from ..models import Freelancer


class PublicFreelancerSerializer(serializers.ModelSerializer):
    """Serializer that exposes information on the freelancer
    appropriate for public use.
    """
    class Meta:
        model = Freelancer
        fields = ('id', 'first_name', 'last_name')

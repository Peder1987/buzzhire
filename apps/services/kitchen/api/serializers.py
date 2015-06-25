from django.forms import widgets
from rest_framework import serializers
from ..models import KitchenFreelancer, KitchenJobRequest
from apps.freelancer.api.serializers import (PrivateFreelancerSerializer,
                                             PublicFreelancerSerializer)
from apps.job.api.serializers import JobRequestSerializer



class PublicKitchenFreelancerSerializer(PublicFreelancerSerializer):
    """Serializer for public views of kitchen."""

    class Meta(PublicFreelancerSerializer.Meta):
        model = KitchenFreelancer
        fields = PublicFreelancerSerializer.Meta.fields + ('role',)


class PrivateKitchenFreelancerSerializer(PrivateFreelancerSerializer):
    """Serializer for the kitchen freelancer's own profile."""

    class Meta:
        model = KitchenFreelancer
        fields = PrivateFreelancerSerializer.Meta.fields + ('role',)



class KitchenJobRequestSerializer(JobRequestSerializer):

    class Meta:
        model = KitchenJobRequest
        fields = JobRequestSerializer.Meta.fields + \
                  ('role',)

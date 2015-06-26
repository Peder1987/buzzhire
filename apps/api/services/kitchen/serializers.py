from django.forms import widgets
from rest_framework import serializers
from apps.services.kitchen.models import KitchenFreelancer, KitchenJobRequest
from ...freelancer.serializers import (PrivateFreelancerSerializer,
                                             FreelancerForClientSerializer)
from ...job.serializers import JobRequestSerializer



class KitchenFreelancerForClientSerializer(FreelancerForClientSerializer):
    """Serializer for public views of kitchen."""

    class Meta(FreelancerForClientSerializer.Meta):
        model = KitchenFreelancer
        fields = FreelancerForClientSerializer.Meta.fields + ('role',)


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

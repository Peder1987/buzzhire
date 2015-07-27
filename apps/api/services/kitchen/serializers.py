from django.forms import widgets
from rest_framework import serializers
from apps.services.kitchen.models import KitchenFreelancer, KitchenJobRequest
from ...freelancer.serializers import (OwnFreelancerSerializer,
                                             FreelancerForClientSerializer)
from ...job.serializers import JobRequestForFreelancerSerializer
from ...booking.serializers import BookingsJobRequestForClientSerializer


class KitchenFreelancerForClientSerializer(FreelancerForClientSerializer):
    """Serializer for public views of kitchen."""

    class Meta(FreelancerForClientSerializer.Meta):
        model = KitchenFreelancer
        fields = FreelancerForClientSerializer.Meta.fields + ('role',)


class PrivateKitchenFreelancerSerializer(OwnFreelancerSerializer):
    """Serializer for the kitchen freelancer's own profile."""

    class Meta:
        model = KitchenFreelancer
        fields = OwnFreelancerSerializer.Meta.fields + ('role',)



class KitchenJobRequestForFreelancerSerializer(JobRequestForFreelancerSerializer):
    class Meta(JobRequestForFreelancerSerializer.Meta):
        model = KitchenJobRequest
        fields = JobRequestForFreelancerSerializer.Meta.fields + \
                  ('role',)

class KitchenJobRequestForClientSerializer(BookingsJobRequestForClientSerializer):
    class Meta(BookingsJobRequestForClientSerializer.Meta):
        model = KitchenJobRequest
        fields = BookingsJobRequestForClientSerializer.Meta.fields + \
                  ('role',)

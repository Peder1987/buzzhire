from django.forms import widgets
from rest_framework import serializers
from apps.services.bar.models import BarFreelancer, BarJobRequest
from ...freelancer.serializers import (PrivateFreelancerSerializer,
                                             FreelancerForClientSerializer)
from ...job.serializers import JobRequestForFreelancerSerializer



class BarFreelancerForClientSerializer(FreelancerForClientSerializer):
    """Serializer for public views of bar."""

    class Meta(FreelancerForClientSerializer.Meta):
        model = BarFreelancer
        fields = FreelancerForClientSerializer.Meta.fields + ('role',)


class PrivateBarFreelancerSerializer(PrivateFreelancerSerializer):
    """Serializer for the bar freelancer's own profile."""

    class Meta:
        model = BarFreelancer
        fields = PrivateFreelancerSerializer.Meta.fields + ('role',)



class BarJobRequestForFreelancerSerializer(JobRequestForFreelancerSerializer):

    class Meta:
        model = BarJobRequest
        fields = JobRequestForFreelancerSerializer.Meta.fields + \
                  ('role',)

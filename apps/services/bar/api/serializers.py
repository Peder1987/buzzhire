from django.forms import widgets
from rest_framework import serializers
from ..models import BarFreelancer, BarJobRequest
from apps.freelancer.api.serializers import (PrivateFreelancerSerializer,
                                             PublicFreelancerSerializer)
from apps.job.api.serializers import JobRequestSerializer



class PublicBarFreelancerSerializer(PublicFreelancerSerializer):
    """Serializer for public views of bar."""

    class Meta(PublicFreelancerSerializer.Meta):
        model = BarFreelancer
        fields = PublicFreelancerSerializer.Meta.fields + ('role',)


class PrivateBarFreelancerSerializer(PrivateFreelancerSerializer):
    """Serializer for the bar freelancer's own profile."""

    class Meta:
        model = BarFreelancer
        fields = PrivateFreelancerSerializer.Meta.fields + ('role',)



class BarJobRequestSerializer(JobRequestSerializer):

    class Meta:
        model = BarJobRequest
        fields = JobRequestSerializer.Meta.fields + \
                  ('role',)

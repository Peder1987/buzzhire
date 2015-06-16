from django.forms import widgets
from rest_framework import serializers
from ..models import VehicleType, FlexibleVehicleType, Driver
from apps.freelancer.api.serializers import PrivateFreelancerSerializer


class VehicleTypeSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField('_name')
    def _name(self, obj):
        return str(obj)

    class Meta:
        model = VehicleType
        fields = ('id', 'name', 'delivery_box_applicable')


class FlexibleVehicleTypeSerializer(VehicleTypeSerializer):
    class Meta:
        model = FlexibleVehicleType
        fields = VehicleTypeSerializer.Meta.fields


class PrivateDriverSerializer(PrivateFreelancerSerializer):
    """Serializer for the driver's own profile."""

#     vehicle_types = serializers.HyperlinkedRelatedField(read_only=True,
#                                     view_name='driver_vehicle_types-detail')

    class Meta:
        model = Driver
        fields = PrivateFreelancerSerializer.Meta.fields + ('driving_experience',)

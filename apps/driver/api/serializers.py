from django.forms import widgets
from rest_framework import serializers
from ..models import VehicleType, FlexibleVehicleType, Driver
from apps.freelancer.api.serializers import OwnFreelancerSerializer
from apps.api.serializers import ChoiceField
from .permissions import DriverOnlyPermission

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


class OwnDriverSerializer(OwnFreelancerSerializer):
    """Serializer for the driver's own profile."""

    permission_classes = (DriverOnlyPermission,)

#     vehicle_types = serializers.HyperlinkedRelatedField(read_only=True,
#                                     view_name='driver_vehicle_types-detail')

    driving_experience = ChoiceField()

    class Meta:
        model = Driver
        fields = OwnFreelancerSerializer.Meta.fields + ('driving_experience',)

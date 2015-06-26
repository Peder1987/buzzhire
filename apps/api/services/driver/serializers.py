from django.forms import widgets
from rest_framework import serializers
from apps.services.driver.models import (VehicleType, FlexibleVehicleType,
                Driver, DriverJobRequest, DriverVehicleType)
from ...freelancer.serializers import (PrivateFreelancerSerializer,
                                             FreelancerForClientSerializer)
from ...job.serializers import JobRequestForFreelancerSerializer


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


class DriverForClientSerializer(FreelancerForClientSerializer):
    """Serializer for public views of driver."""
    vehicles = serializers.SerializerMethodField()
    def get_vehicles(self, obj):
        vehicles_list = []
        for vehicle in obj.drivervehicletype_set.all():
            vehicles_list.append({
                'vehicle_type_name': str(vehicle),
                'own_vehicle': vehicle.own_vehicle,
                'delivery_box': vehicle.delivery_box}
        )
        return vehicles_list

    class Meta(FreelancerForClientSerializer.Meta):
        model = Driver
        fields = FreelancerForClientSerializer.Meta.fields + ('vehicles',
                                                           'phone_type')


class PrivateDriverSerializer(PrivateFreelancerSerializer):
    """Serializer for the driver's own profile."""

#     vehicle_types = serializers.HyperlinkedRelatedField(read_only=True,
#                                     view_name='driver_vehicle_types-detail')

    class Meta:
        model = Driver
        fields = PrivateFreelancerSerializer.Meta.fields + ('phone_type',)



class DriverJobRequestForFreelancerSerializer(JobRequestForFreelancerSerializer):

    flexible_vehicle_type = serializers.HyperlinkedRelatedField(read_only=True,
                                    view_name='flexible_vehicle_types-detail',
                                    source='vehicle_type')
    class Meta:
        model = DriverJobRequest
        fields = JobRequestForFreelancerSerializer.Meta.fields + \
                  ('flexible_vehicle_type', 'minimum_delivery_box',
                   'delivery_box_applicable', 'own_vehicle',
                   'phone_requirement')


class DriverVehicleTypeSerializer(serializers.ModelSerializer):
    """Serializer for driver vehicle types for the logged in driver.
    """
    vehicle_type = serializers.HyperlinkedRelatedField(read_only=True,
                                    view_name='vehicle_types-detail')

    vehicle_type_name = serializers.SerializerMethodField()
    def get_vehicle_type_name(self, obj):
        return str(obj.vehicle_type)

    class Meta:
        model = DriverVehicleType
        fields = ('id', 'vehicle_type', 'vehicle_type_name',
                  'own_vehicle', 'delivery_box')

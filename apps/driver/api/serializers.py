from django.forms import widgets
from rest_framework import serializers
from ..models import VehicleType, FlexibleVehicleType


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

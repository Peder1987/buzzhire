from django.forms import widgets
from rest_framework import serializers
from apps.api.serializers import MoneyField
from ..models import JobRequest
from apps.service.driver.models import DriverJobRequest


class JobRequestSerializer(serializers.ModelSerializer):
    client = serializers.HyperlinkedRelatedField(read_only=True,
                                            view_name='clients-detail')

    address = serializers.SerializerMethodField('_address')
    def _address(self, obj):
        return {
            'address1': obj.address1,
            'address2': obj.address2,
            'city': obj.get_city_display(),
            'postcode': str(obj.postcode),
        }

    freelancer_pay_per_hour = MoneyField()

    class Meta:
        model = JobRequest
        fields = ('id', 'reference_number', 'client', 'status',
                  'tips_included', 'date', 'start_time', 'duration',
                  'end_datetime', 'number_of_freelancers', 'address',
                  'phone_requirement', 'comments', 'freelancer_pay_per_hour')


class DriverJobRequestSerializer(JobRequestSerializer):

    flexible_vehicle_type = serializers.HyperlinkedRelatedField(read_only=True,
                                    view_name='flexible_vehicle_types-detail',
                                    source='vehicle_type')
    class Meta:
        model = DriverJobRequest
        fields = JobRequestSerializer.Meta.fields + \
                  ('flexible_vehicle_type', 'minimum_delivery_box',
                   'delivery_box_applicable',
                   'driving_experience', 'own_vehicle',)

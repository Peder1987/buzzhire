from django.forms import widgets
from rest_framework import serializers
from ..models import JobRequest, DriverJobRequest


class JobRequestSerializer(serializers.ModelSerializer):
    client = serializers.HyperlinkedRelatedField(read_only=True,
                                            view_name='clients-detail')

    status = serializers.SerializerMethodField('_status')
    def _status(self, obj):
        return {
            'value': obj.status,
            'text': obj.get_status_display(),
        }

    address = serializers.SerializerMethodField('_address')
    def _address(self, obj):
        return {
            'address1': obj.address1,
            'address2': obj.address2,
            'city': obj.get_city_display(),
            'postcode': str(obj.postcode),
        }

    phone_requirement = serializers.SerializerMethodField('_phone_requirement')
    def _phone_requirement(self, obj):
        return {
            'value': obj.phone_requirement,
            'text': obj.get_phone_requirement_display(),
        }

    freelancer_pay_per_hour = serializers.SerializerMethodField(
                                                    '_freelancer_pay_per_hour')
    def _freelancer_pay_per_hour(self, obj):
        return {
            'amount': obj.freelancer_pay_per_hour.amount,
            'currency': str(obj.freelancer_pay_per_hour.currency),
        }

    class Meta:
        model = JobRequest
        fields = ('id', 'reference_number', 'client', 'status',
                  'tips_included', 'date', 'start_time', 'duration',
                  'end_datetime', 'number_of_freelancers', 'address',
                  'phone_requirement', 'comments', 'freelancer_pay_per_hour')


class DriverJobRequestSerializer(JobRequestSerializer):
    driving_experience = serializers.SerializerMethodField(
                                                        '_driving_experience')
    def _driving_experience(self, obj):
        return {
            'value': obj.driving_experience,
            'text': obj.get_driving_experience_display(),
        }
    flexible_vehicle_type = serializers.HyperlinkedRelatedField(read_only=True,
                                    view_name='flexible_vehicle_types-detail',
                                    source='vehicle_type')
    class Meta:
        model = DriverJobRequest
        fields = JobRequestSerializer.Meta.fields + \
                  ('flexible_vehicle_type', 'minimum_delivery_box',
                   'delivery_box_applicable',
                   'driving_experience', 'own_vehicle',)

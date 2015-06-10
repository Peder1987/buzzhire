from django.forms import widgets
from rest_framework import serializers
from ..models import JobRequest, DriverJobRequest


class JobRequestSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField('_status')

    def _status(self, obj):
        return {
            'value': obj.status,
            'text': obj.get_status_display(),
        }

    class Meta:
        model = JobRequest
        fields = ('id', 'client', 'status')


class DriverJobRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverJobRequest
        fields = ('id', 'client', 'status', 'driving_experience', 'own_vehicle')

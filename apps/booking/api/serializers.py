from django.forms import widgets
from rest_framework import serializers
from ..models import Booking


class BookingSerializer(serializers.ModelSerializer):
    freelancer = serializers.HyperlinkedRelatedField(read_only=True,
                                            view_name='freelancers-detail')
    job_request = serializers.HyperlinkedRelatedField(read_only=True,
                                            view_name='job_requests-detail',
                                            source='jobrequest')

    class Meta:
        model = Booking
        fields = ('id', 'freelancer', 'job_request', 'created')

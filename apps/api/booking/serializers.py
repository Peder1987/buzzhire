from django.forms import widgets
from rest_framework import serializers
from apps.booking.models import Booking, Invitation
from ..job import serializers as job_serializers

class BookingOrInvitationSerializer(serializers.ModelSerializer):
    "Serializer for Bookings or Invitations, for freelancers."
    job_request = serializers.HyperlinkedRelatedField(read_only=True,
                            view_name='job_requests_for_freelancer-detail',
                            source='jobrequest')

    job_request_full = \
            job_serializers.PolymorphicJobRequestForFreelancerSerializer(
                                                        source='jobrequest',
                                                        read_only=True)

    class Meta:
        fields = ('id', 'reference_number',
                  'job_request', 'date_created',
                  'job_request_full')

class BookingSerializer(BookingOrInvitationSerializer):
    class Meta(BookingOrInvitationSerializer.Meta):
        model = Booking



class InvitationSerializer(BookingOrInvitationSerializer):
    class Meta(BookingOrInvitationSerializer.Meta):
        model = Invitation

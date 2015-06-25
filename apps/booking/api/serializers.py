from django.forms import widgets
from rest_framework import serializers
from ..models import Booking, Invitation


class BookingOrInvitationSerializer(serializers.ModelSerializer):
    "Serializer for Bookings or Invitations."
    # freelancer = serializers.HyperlinkedRelatedField(read_only=True,
    #                                        view_name='freelancers-detail')
    job_request = serializers.HyperlinkedRelatedField(read_only=True,
                                            view_name='job_requests-detail',
                                            source='jobrequest')

    class Meta:
        fields = ('id', 'reference_number',
                  'job_request', 'date_created')

class BookingSerializer(BookingOrInvitationSerializer):
    class Meta(BookingOrInvitationSerializer.Meta):
        model = Booking
        fields = BookingOrInvitationSerializer.Meta.fields


class InvitationSerializer(BookingOrInvitationSerializer):
    class Meta(BookingOrInvitationSerializer.Meta):
        model = Invitation
        fields = BookingOrInvitationSerializer.Meta.fields + ('date_accepted',)

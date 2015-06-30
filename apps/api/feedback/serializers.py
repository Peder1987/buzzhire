from rest_framework import serializers
from ..booking.serializers import BookingForClientSerializer


class BookingAwaitingFeedbackFromClientSerializer(BookingForClientSerializer):
    "A booking that requires feedback from a client."
    job_request = serializers.HyperlinkedRelatedField(
                                    view_name='job_requests_for_client-detail',
                                    read_only=True,
                                    source='jobrequest')

    class Meta(BookingForClientSerializer.Meta):
        fields = BookingForClientSerializer.Meta.fields + ('job_request',)

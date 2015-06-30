from rest_framework import serializers
from apps.feedback.models import BookingFeedback
from ..booking.serializers import BookingForClientSerializer


class BookingAwaitingFeedbackFromClientSerializer(BookingForClientSerializer):
    "A booking that requires feedback from a client."
    job_request = serializers.HyperlinkedRelatedField(
                                    view_name='job_requests_for_client-detail',
                                    read_only=True,
                                    source='jobrequest')

    class Meta(BookingForClientSerializer.Meta):
        fields = BookingForClientSerializer.Meta.fields + ('job_request',)


class FreelancerHyperlinkedField(serializers.HyperlinkedRelatedField):
    """Field linking the freelancer from the feedback."""
    def get_attribute(self, instance):
        return instance.booking.freelancer

class JobRequestHyperlinkedField(serializers.HyperlinkedRelatedField):
    """Field linking the job request from the feedback."""
    def get_attribute(self, instance):
        return instance.booking.jobrequest


class FeedbackByClientSerializer(serializers.ModelSerializer):
    freelancer = FreelancerHyperlinkedField(
                        view_name='freelancers_for_client-detail',
                        read_only=True)
    job_request = JobRequestHyperlinkedField(
                        view_name='job_requests_for_client-detail',
                        read_only=True)
    class Meta:
        model = BookingFeedback
        fields = ('id', 'booking', 'freelancer', 'job_request',
                  'score', 'comment')

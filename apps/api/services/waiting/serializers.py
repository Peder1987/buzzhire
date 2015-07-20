from apps.services.waiting.models import WaitingJobRequest
from ...booking.serializers import BookingsJobRequestForClientSerializer


class WaitingJobRequestForClientSerializer(
                                        BookingsJobRequestForClientSerializer):
    class Meta(BookingsJobRequestForClientSerializer.Meta):
        model = WaitingJobRequest

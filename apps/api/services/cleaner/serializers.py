from apps.services.cleaner.models import CleanerJobRequest
from ...booking.serializers import BookingsJobRequestForClientSerializer


class CleanerJobRequestForClientSerializer(
                                        BookingsJobRequestForClientSerializer):
    class Meta(BookingsJobRequestForClientSerializer.Meta):
        model = CleanerJobRequest

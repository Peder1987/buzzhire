from rest_framework import viewsets
from ..client.permissions import ClientOnlyPermission
from apps.feedback.models import get_bookings_awaiting_feedback_for_client
from .serializers import BookingAwaitingFeedbackFromClientSerializer


class ClientFeedbackBacklogViewSet(viewsets.ReadOnlyModelViewSet):
    """List of bookings awaiting feedback for the current client.
    
    ## Fields
    
    - `id` Unique id for the booking. Integer.
    - `reference_number` Public reference number for the booking.
    - `freelancer` Freelancer endpoint.  
    - `date_created` Date and time of when the booking was created.
    - `job_request` Endpoint of job request the booking is for.     
    """
    serializer_class = BookingAwaitingFeedbackFromClientSerializer

    permission_classes = (ClientOnlyPermission,)

    def get_queryset(self):
        return get_bookings_awaiting_feedback_for_client(
                                                    self.request.user.client)
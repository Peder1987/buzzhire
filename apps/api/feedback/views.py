from rest_framework import viewsets, mixins
from ..client.permissions import ClientOnlyPermission
from apps.feedback.models import (get_bookings_awaiting_feedback_for_client,
                                  BookingFeedback)
from .serializers import (BookingAwaitingFeedbackFromClientSerializer,
                          FeedbackByClientSerializer)

class FeedbackByClientViewSet(mixins.CreateModelMixin,
                              viewsets.ReadOnlyModelViewSet):
    """List of items of feedback authored by the currently logged in client.
    
    ## Fields
    
    - `id` Unique id.  Read only.
    - `booking` Unique id of the booking the feedback is about.
    - `freelancer` Endpoint for the freelancer the feedback is about.
      Read only.
    - `job_request` Endpoint for the job request the feedback is about.
       Read only.
    - `score` The score, between 1 and 5.  Integer.
    - `comment` Comment about the freelancer.  Free text, optional. 
    
    ## Creating feedback
    
    To create feedback, POST `booking`, `score` and (optionally) `comment`
    to this endpoint.
    
    Clients may only leave feedback on bookings for job requests they own,
    and that they have not already left feedback for.
    
    To see which bookings are awaiting feedback, use the
    `client/bookings/awaiting-feedback` endpoint. 
    
    
    """
    serializer_class = FeedbackByClientSerializer

    permission_classes = (ClientOnlyPermission,)

    def get_queryset(self):
        return BookingFeedback.objects.feedback_by_client(
                                                    self.request.user.client)


class ClientFeedbackBacklogViewSet(viewsets.ReadOnlyModelViewSet):
    """List of bookings awaiting feedback for the current client.

    To create feedback, see the `client/feedback` endpoint.
    
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

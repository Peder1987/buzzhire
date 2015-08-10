from django.db.models import Q
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from ..freelancer.permissions import FreelancerOnlyPermission
from .serializers import BookingSerializer, InvitationSerializer
from apps.booking.models import (Booking, Invitation,
                            JobAlreadyBookedByFreelancer, JobFullyBooked)


class BookingForFreelancerViewSet(viewsets.ReadOnlyModelViewSet):
    """All bookings for the currently logged in freelancer.
    
    Note: you must be logged in as a freelancer.

    ## Query parameters
    
    - `dateslice` Optional. Limit results by date.  Choices are:
        - `past` All past bookings for the Freelancer.
        - `future` All future bookings for the Freelancer.
    
    ## Fields
    
    - `id` Unique id for the booking. Integer. Read only.
    - `reference_number` Public reference number for the booking.  Read only.
    - `job_request` API URL for the job request the booking is for.  
    - `date_created` Date and time of when the booking was created.
    """
    serializer_class = BookingSerializer

    permission_classes = (FreelancerOnlyPermission,)

    def get_queryset(self):
        queryset = Booking.objects.for_freelancer(self.request.user.freelancer)
        if self.request.GET.get('dateslice') == 'future':
            queryset = queryset.future()
        elif self.request.GET.get('dateslice') == 'past':
            queryset = queryset.past()
        return queryset


class InvitationForFreelancerViewSet(viewsets.ReadOnlyModelViewSet):
    """All invitations that can be applied to by the currently
    logged in freelancer.
    
    Note: you must be logged in as a freelancer.
    
    ## Fields
    
    - `id` Unique id for the invitation. Integer. Read only.
    - `reference_number` Public reference number for the invitation.  Read only.
    - `job_request` API URL for the job request the invitation is for.  
    - `date_created` Date and time of when the invitation was created.
    - `accept_endpoint` The API endpoint to POST to in order to
      accept the invitation.
      
    ## Accepting invitations
    
    To accept an invitation, POST to the `accept_endpoint` provided.  No data
    is required.
    
    If the invitation can be accepted, it will return the booking that was
    created.
    
    Invitations are not guaranteed to stay valid - for example, if a job is
    becomes fully booked.  If the invitation is no longer valid, the response
    will be a 404.
    """
    serializer_class = InvitationSerializer

    permission_classes = (FreelancerOnlyPermission,)

    def get_queryset(self):
        return Invitation.objects.can_be_applied_to_by_freelancer(
                                                self.request.user.freelancer)

    @detail_route(methods=['post'])
    def accept(self, request, pk=None):

        invitation = self.get_object()

        # Validation - at present the validation already happens in
        # get_queryset(), but we may want to give more specific feedback (as
        # it will just say 'Not found' if it can't find the invitation.
#         try:
#             invitation.validate_can_be_accepted()
#         except JobFullyBooked:
#             return Response('This job request is now fully booked.',
#                             status=status.HTTP_400_BAD_REQUEST)
#         except JobAlreadyBookedByFreelancer:
#             # This shouldn't happen, but just in case
#             return Response('This job request has already been accepted' \
#                             'by the freelancer.',
#                             status=status.HTTP_400_BAD_REQUEST)

        # TODO - consider potential race condition here?

        booking = Booking.objects.create(jobrequest=invitation.jobrequest,
                                         freelancer=invitation.freelancer)

        serializer = BookingSerializer(booking,
                                       context={'request': self.request})
        return Response(serializer.data)

from django.db.models import Q
from rest_framework import viewsets
from apps.freelancer.api.permissions import FreelancerOnlyPermission
from .serializers import BookingSerializer, InvitationSerializer
from ..models import Booking, Invitation


class FreelancerBookingViewSet(viewsets.ReadOnlyModelViewSet):
    """All bookings for the currently logged in freelancer.
    
    Note: you must be logged in as a freelancer.
    
    ## Fields
    
    - `id` Unique id for the booking. Integer. Read only.
    - `reference_number` Public reference number for the booking.  Read only.
    - `job_request` API URL for the job request the booking is for.  
    - `date_created` Date and time of when the booking was created.
    """
    serializer_class = BookingSerializer

    permission_classes = (FreelancerOnlyPermission,)

    def get_queryset(self):
        return Booking.objects.for_freelancer(self.request.user.freelancer)


class FreelancerInvitationViewSet(viewsets.ReadOnlyModelViewSet):
    """All open invitations for the currently logged in freelancer.
    
    Note: you must be logged in as a freelancer.
    
    ## Fields
    
    - `id` Unique id for the invitation. Integer. Read only.
    - `reference_number` Public reference number for the invitation.  Read only.
    - `job_request` API URL for the job request the invitation is for.  
    - `date_created` Date and time of when the invitation was created.
    """
    serializer_class = InvitationSerializer

    permission_classes = (FreelancerOnlyPermission,)

    def get_queryset(self):
        return Invitation.objects.open_for_freelancer(self.request.user.freelancer)

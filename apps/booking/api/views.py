from django.db.models import Q
from rest_framework import viewsets
from apps.freelancer.api.permissions import FreelancerOnlyPermission
from .serializers import BookingSerializer
from ..models import Booking


class FreelancerBookingViewSet(viewsets.ReadOnlyModelViewSet):
    """All bookings for the currently logged in freelancer.
    
    Note: you must be logged in as a freelancer.
    """
    serializer_class = BookingSerializer

    permission_classes = (FreelancerOnlyPermission,)

    def get_queryset(self):
        return Booking.objects.for_freelancer(self.request.user.freelancer)

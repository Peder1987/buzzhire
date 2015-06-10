from django.db.models import Q
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import BookingSerializer
from ..models import Booking


class FreelancerBookingViewSet(viewsets.ReadOnlyModelViewSet):
    "All bookings for the currently logged in freelancer."
    serializer_class = BookingSerializer

    # TODO - require the user to be a freelancer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Booking.objects.for_freelancer(self.request.user.freelancer)

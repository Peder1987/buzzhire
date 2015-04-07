from django.views.generic import ListView, UpdateView
from django.core.urlresolvers import reverse_lazy
from apps.core.views import ContextMixin, TabsMixin
from apps.freelancer.views import FreelancerOnlyMixin
from .models import Booking, Availability
from .forms import AvailabilityForm


class FreelancerBookingsList(FreelancerOnlyMixin,
                             ContextMixin, TabsMixin, ListView):
    """List of bookings assigned to a freelancer.
    This view has two modes - if self.past is True, it will return the
    job requests in the past, otherwise it will show upcoming job requests.   
    """
    paginate_by = 2
    extra_context = {'title': 'My bookings'}
    tabs = [
        ('Upcoming', reverse_lazy('freelancer_bookings_list')),
        ('Past', reverse_lazy('freelancer_bookings_list_past')),
    ]
    past = False

    def get_queryset(self, *args, **kwargs):
        queryset = Booking.objects.for_freelancer(self.freelancer)
        if self.past:
            return queryset.past()
        else:
            return queryset.future()


class AvailabilityUpdate(FreelancerOnlyMixin,
                         ContextMixin, UpdateView):
    """View for freelancer to edit their availability.
    """
    model = Availability
    extra_context = {'title': 'Availability'}
    form_class = AvailabilityForm

    def get_object(self):
        # Return the Availability for the Freelancer, creating one
        # if it doesn't exist.
        try:
            return self.freelancer.availability
        except Availability.DoesNotExist:
            return Availability.objects.create(freelancer=self.freelancer)


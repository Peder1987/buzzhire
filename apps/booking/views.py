from django.views.generic import ListView, UpdateView
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from apps.account.views import AdminOnlyMixin
from apps.core.views import ContextMixin, TabsMixin
from apps.freelancer.views import FreelancerOnlyMixin
from .models import Booking, Availability
from .forms import AvailabilityForm, JobMatchingForm


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
    success_url = reverse_lazy('availability_update')

    def get_object(self):
        # Return the Availability for the Freelancer, creating one
        # if it doesn't exist.
        try:
            return self.freelancer.availability
        except Availability.DoesNotExist:
            return Availability.objects.create(freelancer=self.freelancer)

    def form_valid(self, *args, **kwargs):
        messages.add_message(self.request, messages.INFO, 'Saved.')
        return super(AvailabilityUpdate, self).form_valid(*args, **kwargs)


class JobMatchingView(AdminOnlyMixin, ContextMixin, ListView):
    """View for searching drivers to match with jobs.
    """
    template_name = 'booking/job_matching.html'
    paginate_by = 50
    extra_context = {'title': 'Job matching'}

    def get(self, request, *args, **kwargs):
        # We use a form, but with the GET method as it's a search form.
        if self.request.GET.get('search', None):
            # A search has been made
            self.form = JobMatchingForm(self.request.GET)
        else:
            # No search made yet
            self.form = JobMatchingForm()
        return super(JobMatchingView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        "Called first by get()."
        # Return the object_list, but only if the search form validates
        if self.form.is_valid():
            return self.form.get_results()
        return []

    def get_context_data(self, **kwargs):
        context = super(JobMatchingView, self).get_context_data(**kwargs)
        context['form'] = self.form
        if self.form.is_valid():
            # Set a searched flag to let the template know a search has run
            context['searched'] = True
        return context

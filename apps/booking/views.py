from django.views.generic import ListView, UpdateView, CreateView, FormView
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from apps.account.views import AdminOnlyMixin
from apps.core.views import ContextMixin, TabsMixin, ContextTemplateView, \
    ConfirmationMixin
from apps.driver.models import Driver
from apps.freelancer.views import FreelancerOnlyMixin
from apps.job.models import DriverJobRequest
from .models import Booking, Availability
from .forms import AvailabilityForm, JobMatchingForm, BookingConfirmForm
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404, redirect


class FreelancerBookingsList(FreelancerOnlyMixin,
                             ContextMixin, TabsMixin, ListView):
    """List of bookings assigned to a freelancer.
    This view has two modes - if self.past is True, it will return the
    job requests in the past, otherwise it will show upcoming job requests.   
    """
    paginate_by = 2
    extra_context = {'title': 'Bookings'}
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


class AvailabilityUpdate(FreelancerOnlyMixin, SuccessMessageMixin,
                         ContextMixin, UpdateView):
    """View for freelancer to edit their availability.
    """
    model = Availability
    extra_context = {'title': 'Availability'}
    form_class = AvailabilityForm
    success_url = reverse_lazy('availability_update')
    success_message = 'Saved.'

    def get_object(self):
        # Return the Availability for the Freelancer, creating
        # (but not saving) one if it doesn't exist.
        try:
            return self.freelancer.availability
        except Availability.DoesNotExist:
            return Availability(freelancer=self.freelancer)


class JobMatchingView(AdminOnlyMixin, ContextMixin, ListView):
    """View for searching drivers to match with jobs.
    """
    template_name = 'booking/job_matching.html'
    paginate_by = 50
    extra_context = {'title': 'Job matching'}

    def get(self, request, *args, **kwargs):
        # We use a form, but with the GET method as it's a search form.

        # First, handle the job request pk which may have been passed
        # via the url.  If this is present, we should instantiate the form
        # with that job request
        job_request_pk = kwargs.get('job_request_pk', None)
        if job_request_pk:
            self.job_request = get_object_or_404(DriverJobRequest,
                                                 pk=job_request_pk)
            form_kwargs = {'job_request': self.job_request}
        else:
            form_kwargs = {}

        if self.request.GET.get('search', None):
            # A search has been made
            form_kwargs['data'] = self.request.GET

        self.form = JobMatchingForm(**form_kwargs)

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


class BookingConfirm(AdminOnlyMixin, ConfirmationMixin, FormView):
    """Confirmation form for the creation of a Booking
    - i.e. assigning a freelancer to a job.
    """
    extra_context = {'title': 'Create booking'}
    question = 'Are you sure you want to create this booking?'
    cancel_url = reverse_lazy('account_dashboard')
    template_name = 'account/dashboard_base.html'
    form_class = BookingConfirmForm


    def dispatch(self, *args, **kwargs):
        self.job_request = get_object_or_404(DriverJobRequest,
                                             pk=kwargs.pop('job_request_pk'))
        self.driver = get_object_or_404(Driver,
                                             pk=kwargs.pop('driver_pk'))
        return super(BookingConfirm, self).dispatch(*args, **kwargs)


    def get_form_kwargs(self, *args, **kwargs):
        # Pass the job request and freelancer to the form
        form_kwargs = super(BookingConfirm, self).get_form_kwargs(*args,
                                                                  **kwargs)
        form_kwargs.update({
            'job_request': self.job_request,
            'driver': self.driver,
        })
        return form_kwargs

    def form_valid(self, *args, **kwargs):
        Booking.objects.create(freelancer=self.driver,
                               jobrequest=self.job_request)
        messages.success(self.request, 'Created booking.')
        return redirect(self.job_request.get_absolute_url())


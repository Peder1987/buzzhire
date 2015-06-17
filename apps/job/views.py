from django.views.generic import (CreateView, UpdateView, TemplateView,
                            ListView, DetailView, FormView)
from django.views.generic.detail import SingleObjectMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy, reverse
from allauth.account import app_settings
from allauth.account.utils import complete_signup
from django.shortcuts import redirect
from braces.views._access import AnonymousRequiredMixin
from apps.core.views import ContextMixin, TabsMixin, ConfirmationMixin, \
                                            GrantCheckingMixin
from apps.account.views import AdminOnlyMixin
from apps.client.views import ClientOnlyMixin, OwnedByClientMixin
from apps.client.forms import ClientInnerForm
from apps.client.models import Client
from apps.freelancer.models import Freelancer
from apps.account.views import SignupView as BaseSignupView
from . import signals
from .models import JobRequest
from apps.service.driver.models import DriverJobRequest
from .forms import DriverJobRequestForm, DriverJobRequestInnerForm, \
                    DriverJobRequestSignupInnerForm, JobRequestCheckoutForm
from django.http.response import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from . import services, service_from_job_request


class DriverJobRequestCreate(ClientOnlyMixin, ContextMixin, CreateView):
    "Creation page for submitting a driver job request."
    extra_context = {'title': 'Book a driver'}
    model = DriverJobRequest
    form_class = DriverJobRequestForm
    template_name = 'job/driverjobrequest_create.html'

    def dispatch(self, request, *args, **kwargs):
        # if not logged in, redirect to a job request pre-sign up page
        if request.user.is_anonymous():
            return redirect('driverjobrequest_create_anon')
        return super(DriverJobRequestCreate, self).dispatch(request, *args,
                                                            **kwargs)

    def get_success_url(self):
        return reverse('driverjobrequest_checkout', args=(self.object.pk,))

    def form_valid(self, form):
        """Adapted version of ModelFormMixin.form_valid
        that supplies the client.
        """
        self.object = form.save(client=self.client)
        return HttpResponseRedirect(self.get_success_url())


class DriverJobRequestCreateAnonymous(BaseSignupView):
    "Page for anonymous users who want to create a job request."
    template_name = 'job/driverjobrequest_create_anon.html'
    extra_context = {'title': 'Book a driver'}
    form_class = DriverJobRequestSignupInnerForm
    # The form prefix for the account form
    prefix = 'account'

    extra_forms = {
        'client': ClientInnerForm,
        'driverjobrequest': DriverJobRequestInnerForm,
    }

    def get_context_data(self, *args, **kwargs):
        context = super(DriverJobRequestCreateAnonymous, self).get_context_data(*args, **kwargs)
        context['extra_forms'] = []
        for prefix, form_class in self.extra_forms.items():
            context['extra_forms'].append(self.get_form(form_class, prefix))
        return context

    def get_form(self, form_class, prefix=None):
        # Passes the prefix through to get_form_kwargs
        return form_class(**self.get_form_kwargs(prefix))

    def get_form_kwargs(self, prefix=None):
        """Standard get_form_kwargs() method adapted to return
        the extra forms too."""

        if prefix is None:
            # This is for the main form (signup form)
            prefix = self.get_prefix()

        kwargs = {
            'initial': self.get_initial(),
            'prefix': prefix,
        }

        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def post(self, request, *args, **kwargs):
        "Standard post method adapted to validate both forms."
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        self.bound_forms = {self.get_prefix(): form}
        for prefix, form_class in self.extra_forms.items():
            self.bound_forms[prefix] = self.get_form(form_class, prefix)

        if all([f.is_valid() for f in self.bound_forms.values()]):
            # If all the forms validate
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        """Adapted from BaseSignupView to save the driver too.
        We do not currently run the complete_signup process, as we
        don't want the driver to be logged in after sign up. 
        """
        user = form.save(self.request)
        # Save extra forms too
        client = self.bound_forms['client'].save(user=user)
        self.driverjobrequest = self.bound_forms['driverjobrequest'].save(
                                                                client=client)
        # Send signal (see DriverJobRequestCreate for explanation)
        signals.driverjobrequest_created.send(sender=self.__class__,
                                      driverjobrequest=self.driverjobrequest)
        return complete_signup(self.request, user,
                               app_settings.EMAIL_VERIFICATION,
                               self.get_success_url())

    def get_success_url(self):
        return reverse('driverjobrequest_checkout',
                       args=(self.driverjobrequest.pk,))



class RequestedJobList(ClientOnlyMixin, ContextMixin, TabsMixin, ListView):
    """List of driver job requests ordered by a client.
    This view has two modes - if self.past is True, it will return the
    job requests in the past, otherwise it will show upcoming job requests.   
    """
    paginate_by = 15
    extra_context = {'title': 'Requested jobs'}
    tabs = [
        ('Upcoming', reverse_lazy('requested_jobs')),
        ('Past', reverse_lazy('requested_jobs_past')),
    ]
    past = False

    def get_queryset(self, *args, **kwargs):
        queryset = DriverJobRequest.objects.for_client(self.client)
        if self.past:
            return queryset.past()
        else:
            return queryset.future()


class JobRequestDetail(GrantCheckingMixin, DetailView):
    """Detail page for job requests.
    We use the GrantCheckingMixin as we want other apps that this app
    doesn't know about (e.g. bookings) to grant certain freelancers access.
    """
    model = JobRequest
    require_login = True
    allow_admin = True
    grant_methods = ['is_owned_by_client']

    def is_owned_by_client(self):
        """Grant method - returns True if the user is a client, and they
        own the job request.
        """
        try:
            self.client = self.request.user.client
        except Client.DoesNotExist:
            self.client = False
        else:
            return self.object.client == self.client

    def get_context_data(self, *args, **kwargs):
        context = super(JobRequestDetail, self).get_context_data(*args,
                                                                       **kwargs)
        context['title'] = self.object
        context['client'] = self.client
        return context



class JobRequestUpdate(AdminOnlyMixin, SuccessMessageMixin, UpdateView):
    "Edit page for job requests."
    model = JobRequest
    success_message = 'Saved.'

    def get_form_class(self):
        # Return the form registered on the service as job_request_edit_form
        service = service_from_job_request(self.object)
        return service.job_request_edit_form

    def get_context_data(self, *args, **kwargs):
        context = super(JobRequestUpdate, self).get_context_data(*args,
                                                                 **kwargs)
        context['title'] = 'Edit %s' % self.object
        return context


class DriverJobRequestCheckout(OwnedByClientMixin, SingleObjectMixin,
                               FormView):
    "Checkout page where client pays for and opens the job request."
    model = DriverJobRequest
    template_name = 'job/driverjobrequest_checkout.html'
    form_class = JobRequestCheckoutForm

    def dispatch(self, *args, **kwargs):
        self.object = self.get_object()
        if self.object.status != DriverJobRequest.STATUS_CHECKOUT:
            return redirect(self.object.get_absolute_url())
        return super(DriverJobRequestCheckout, self).dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(DriverJobRequestCheckout, self).get_context_data(*args,
                                                                    **kwargs)
        context['title'] = 'Confirm and pay'
        return context

    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super(DriverJobRequestCheckout,
                            self).get_form_kwargs(*args, **kwargs)
        # Pass the job request to the form
        # import pdb; pdb.set_trace()
        form_kwargs['instance'] = self.object
        return form_kwargs

    def form_valid(self, form):
        form.save()
        return super(DriverJobRequestCheckout, self).form_valid(form)

    def get_success_url(self):
        # Redirect to confirmation page
        return reverse('driverjobrequest_done', args=(self.object.pk,))

# class DriverJobRequestForFreelancerList(FreelancerOnlyMixin, ListView):
#     """List of driver job requests accepted by a freelancer."""
#     paginate_by = 2
#
#     def get_queryset(self, *args, **kwargs):
#         return DriverJobRequest.objects.for_freelancer(self.freelancer)

class DriverJobRequestDone(OwnedByClientMixin, ContextMixin, DetailView):
    "Confirmation page on successful driver job request submission."
    template_name = 'job/driverjobrequest_done.html'
    extra_context = {'title': 'Thanks for your booking'}
    model = DriverJobRequest


class AdminJobList(AdminOnlyMixin, ContextMixin, TabsMixin, ListView):
    """List of job requests for admin users.
    """
    paginate_by = 15
    extra_context = {'title': 'Job requests'}

    def get_tabs(self):
        "Returns a list of two-tuples for the tabs."
        tabs = []
        for status_value, status_title in JobRequest.STATUS_CHOICES:
            tabs.append((status_title,
                         reverse('job_request_admin_list_tab',
                                 kwargs={'status': status_value})))
        return tabs

    def get_queryset(self, *args, **kwargs):

        return JobRequest.objects.filter(
                    status=self.kwargs.get('status',
                                           JobRequest.STATUS_OPEN))

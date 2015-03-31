from django.views.generic import CreateView, UpdateView, TemplateView
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from braces.views._access import AnonymousRequiredMixin
from apps.core.views import ContextMixin, TabsMixin, ConfirmationMixin
from apps.client.views import ClientOnlyMixin
from .models import DriverJobRequest
from .forms import DriverJobRequestForm


class DriverJobRequestCreate(ClientOnlyMixin, ContextMixin, CreateView):
    "Creation page for submitting a driver job request."
    extra_context = {'title': 'Book a driver'}
    model = DriverJobRequest
    success_url = reverse_lazy('driverjobrequest_complete')
    form_class = DriverJobRequestForm
    template_name = 'account/dashboard_base.html'

    def dispatch(self, request, *args, **kwargs):
        # if not logged in, redirect to a job request pre-sign up page
        if request.user.is_anonymous():
            return redirect('driverjobrequest_create_anon')
        return super(DriverJobRequestCreate, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        form_kwargs = super(DriverJobRequestCreate, self).get_form_kwargs()
        # Pass the logged in user as the client
        form_kwargs['client'] = self.request.user
        return form_kwargs


class DriverJobRequestCreateAnonymous(AnonymousRequiredMixin,
                          ContextMixin, TemplateView):
    "Page for anonymous users who want to create a job request."
    template_name = 'job/driverjobrequest_create_anon.html'
    extra_context = {'title': 'Book a driver'}


class DriverJobRequestComplete(ClientOnlyMixin, ContextMixin, TemplateView):
    "Confirmation page on successful driver job request submission."
    template_name = 'job/complete.html'
    extra_context = {'title': 'Thanks for your booking'}

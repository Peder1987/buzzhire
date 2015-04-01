from django.views.generic import CreateView, UpdateView, TemplateView
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from allauth.account import app_settings
from allauth.account.utils import complete_signup
from django.shortcuts import redirect
from braces.views._access import AnonymousRequiredMixin
from apps.core.views import ContextMixin, TabsMixin, ConfirmationMixin
from apps.client.views import ClientOnlyMixin
from apps.client.forms import ClientInnerForm
from apps.account.views import SignupView as BaseSignupView

from .models import DriverJobRequest
from .forms import DriverJobRequestForm, DriverJobRequestInnerForm, \
                    DriverJobRequestSignupInnerForm
from django.http.response import HttpResponseRedirect


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

    def form_valid(self, form):
        """Adapted version of form_valid that supplies the client
        """
        self.object = form.save(client=self.client)
        return HttpResponseRedirect(self.get_success_url())


class DriverJobRequestComplete(ClientOnlyMixin, ContextMixin, TemplateView):
    "Confirmation page on successful driver job request submission."
    template_name = 'job/complete.html'
    extra_context = {'title': 'Thanks for your booking'}


class DriverJobRequestCreateAnonymous(BaseSignupView):
    "Page for anonymous users who want to create a job request."
    template_name = 'job/driverjobrequest_create_anon.html'
    extra_context = {'title': 'Book a driver'}
    form_class = DriverJobRequestSignupInnerForm
    # The form prefix for the account form
    prefix = 'account'
    success_url = reverse_lazy('driverjobrequest_complete')
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
        self.bound_forms['driverjobrequest'].save(client=client)
        return complete_signup(self.request, user,
                               app_settings.EMAIL_VERIFICATION,
                               self.get_success_url())

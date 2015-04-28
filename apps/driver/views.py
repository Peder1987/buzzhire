from django.shortcuts import redirect
from django.core.urlresolvers import reverse_lazy, reverse
from django.views.generic import (DetailView, UpdateView, ListView,
                                CreateView, DeleteView)
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.contrib.auth.views import redirect_to_login
from django.contrib.messages.views import SuccessMessageMixin
from django.conf import settings
from allauth.account.utils import complete_signup
from allauth.account import app_settings
from apps.core.views import ContextMixin, OwnerOnlyMixin, ConfirmationMixin
from apps.account.views import SignupView as BaseSignupView, AdminOnlyMixin
from apps.account.forms import SignupInnerForm
from . import forms
from .models import Driver, DriverVehicleType


class DriverOnlyMixin(object):
    """Views mixin - only allow drivers to access.
    Adds driver as an attribute on the view.
    """
    def dispatch(self, request, *args, **kwargs):
        # If the user is not logged in, give them the chance to
        if self.request.user.is_anonymous():
            return redirect_to_login(self.request.path)
        try:
            self.driver = self.request.user.driver
        except Driver.DoesNotExist:
            raise PermissionDenied
        return super(DriverOnlyMixin, self).dispatch(request,
                                                         *args, **kwargs)


class OwnedByDriverMixin(DriverOnlyMixin, OwnerOnlyMixin):
    """Views mixin - only allow drivers who own the object in question to
    access the view.
    """
    def is_owner(self):
        "Whether or not the current user should be treated as the 'owner'."
        return self.get_object().driver == self.driver


class SignupView(BaseSignupView):
    extra_context = {'title': 'Driver sign up'}
    form_class = SignupInnerForm
    template_name = 'driver/signup.html'
    # The form prefix for the account form
    prefix = 'account'
    success_url = reverse_lazy('driver_thankyou')

    def get_context_data(self, *args, **kwargs):
        context = super(SignupView, self).get_context_data(*args, **kwargs)
        context['driver_form'] = self.get_driver_form()

        return context

    def get_driver_form(self):
        return forms.SignupFormDriverDetails(**self.get_driver_form_kwargs())

    def get_driver_form_kwargs(self):
        """Standard get_form_kwargs() method adapted for the driver form."""

        kwargs = {
            'initial': self.get_initial(),
            'prefix': 'driver',
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
        self.driver_form = self.get_driver_form()
        if form.is_valid() and self.driver_form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        """Adapted from BaseSignupView to save the driver too.
        """

        user = form.save(self.request)
        # Save driver form too
        self.driver_form.save(user)
        if settings.COMING_SOON:
            # Do not log them in
            return redirect('driver_thankyou')
        else:
            return complete_signup(self.request, user,
                               app_settings.EMAIL_VERIFICATION,
                               self.get_success_url())


class DriverDetailView(AdminOnlyMixin, DetailView):
    """Detail view for admin to look at a Driver.
    """
    model = Driver

    def get_context_data(self, *args, **kwargs):
        context = super(DriverDetailView, self).get_context_data(*args,
                                                                 **kwargs)
        context['title'] = self.object.get_full_name()
        return context


class DriverUpdateView(OwnerOnlyMixin, ContextMixin,
                       SuccessMessageMixin, UpdateView):
    "Profile edit page for drivers."
    model = Driver
    form_class = forms.DriverForm
    template_name = 'account/dashboard_base.html'
    success_url = reverse_lazy('account_dashboard')
    extra_context = {'title': 'Edit profile'}
    success_message = 'Saved.'


class DriverVehicleTypeListView(DriverOnlyMixin, ContextMixin, ListView):
    """List of a driver's DriverVehicleTypes - i.e. information about which
    vehicles they can drive/own."""
    model = DriverVehicleType
    extra_context = {'title': 'Vehicles'}

    def get_queryset(self, *args, **kwargs):
        "List only the driver's own vehicles."
        return DriverVehicleType.objects.filter(driver=self.driver)


class DriverVehicleTypeFormViewMixin(DriverOnlyMixin, ContextMixin,
                                     SuccessMessageMixin):
    "Views mixin for create/update pages for driver vehicles."
    model = DriverVehicleType
    form_class = forms.DriverVehicleTypeForm
    template_name = 'driver/vehicles_subpage.html'
    success_message = 'Created.'

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(DriverVehicleTypeFormViewMixin, self).get_form_kwargs(
                                                            *args, **kwargs)
        kwargs['driver'] = self.driver
        return kwargs


class DriverVehicleTypeCreateView(DriverVehicleTypeFormViewMixin, CreateView):
    """Creation page for a driver vehicle."""
    success_url = reverse_lazy('drivervehicletype_list')
    extra_context = {'title': 'Create vehicle'}


class DriverVehicleTypeUpdateView(OwnedByDriverMixin,
                                  DriverVehicleTypeFormViewMixin, UpdateView):
    """Edit page for a driver vehicle."""
    success_url = reverse_lazy('drivervehicletype_list')
    extra_context = {'title': 'Edit vehicle'}


class DriverVehicleTypeDeleteView(OwnedByDriverMixin, ContextMixin,
                                  ConfirmationMixin, DeleteView):
    "Confirmation page for deleting a driver vehicle."
    extra_context = {'title': 'Remove vehicle?'}
    question = 'Are you sure you want to remove this vehicle?'
    model = DriverVehicleType
    template_name = 'driver/vehicles_subpage.html'
    success_message = 'Deleted.'
    success_url = reverse_lazy('drivervehicletype_list')

    def get_cancel_url(self):
        return reverse('drivervehicletype_change', args=(self.object.pk,))

    def delete(self, *args, **kwargs):
        response = super(DriverVehicleTypeDeleteView, self).delete(*args,
                                                                   **kwargs)
        messages.success(self.request, 'Deleted.')
        return response

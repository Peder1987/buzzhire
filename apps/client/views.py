from django.views.generic import CreateView, UpdateView, DetailView
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.contrib.auth.views import redirect_to_login
from apps.core.views import ContextMixin, OwnerOnlyMixin
from . import forms
from .models import Client


class ClientOnlyMixin(object):
    """Views mixin - only allow clients or admins to access."""
    def dispatch(self, request, *args, **kwargs):
        # If the user is not logged in, give them the chance to
        if self.request.user.is_anonymous():
            return redirect_to_login(self.request.path)
        elif not (self.request.user.is_client or self.request.user.is_admin):
            raise PermissionDenied
        return super(ClientOnlyMixin, self).dispatch(request, *args, **kwargs)


class LeadCreateView(ContextMixin, CreateView):
    "The 'express interest' view, for anonymous users to create a Lead."

    extra_context = {'title': 'Express interest'}
    form_class = forms.LeadForm
    template_name = 'client/express_interest.html'
    success_url = reverse_lazy('express_interest_thankyou')


class ClientUpdateView(OwnerOnlyMixin, ContextMixin, UpdateView):
    """View for clients to edit their own profiles.
    """
    model = Client
    form_class = forms.ClientForm
    template_name = 'account/dashboard_base.html'
    success_url = reverse_lazy('account_dashboard')
    extra_context = {'title': 'Edit your profile'}

    def form_valid(self, form):
        response = super(ClientUpdateView, self).form_valid(form)
        messages.add_message(self.request, messages.SUCCESS, 'Saved.')
        return response



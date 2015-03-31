from django.views.generic import CreateView, UpdateView
from django.contrib import messages
from apps.core.views import ContextMixin, OwnerOnlyMixin
from . import forms
from .models import Client
from django.core.urlresolvers import reverse_lazy


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

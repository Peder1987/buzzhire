from django.views.generic import CreateView
from apps.core.views import ContextMixin
from . import forms
from django.core.urlresolvers import reverse_lazy


class LeadCreateView(ContextMixin, CreateView):
    "The 'express interest' view, for anonymous users to create a Lead."

    extra_context = {'title': 'Express interest'}
    form_class = forms.LeadForm
    template_name = 'form_page.html'
    success_url = reverse_lazy('express_interest_thankyou')

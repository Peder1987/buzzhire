from django import forms
from apps.core.forms import CrispyFormMixin
from .models import Lead


class LeadForm(CrispyFormMixin, forms.ModelForm):
    """A form for filling out an expression of interest.
    """
    submit_text = 'Keep me posted'
    submit_context = {'icon_name': 'confirm'}
    class Meta:
        model = Lead
        exclude = ('created',)


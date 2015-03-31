from django import forms
from django.forms import widgets
from .models import DriverJobRequest
from apps.core.forms import CrispyFormMixin, ConfirmForm
from crispy_forms import layout
from django.core.exceptions import ValidationError
from django.forms.widgets import HiddenInput


class DriverJobRequestForm(CrispyFormMixin, forms.ModelForm):
    """Form for submitting a job request.
    Should be instantiated with a Client object.
    """
    submit_text = 'Book'
    submit_context = {'icon_name': 'driverjobrequest_create'}
    def __init__(self, *args, **kwargs):
        self.client = kwargs.pop('client')

        super(DriverJobRequestForm, self).__init__(*args, **kwargs)

        self.fields['client'].widget = HiddenInput()
        self.fields['client'].initial = self.client

    def save(self, commit=True):
        # Make sure the client is saved in the job request
        self.instance.client = self.client
        return super(DriverJobRequestForm, self).save(commit)

    class Meta:
        model = DriverJobRequest
        exclude = 'status',

from django import forms
from django.forms import widgets
from .models import DriverJobRequest
from apps.core.forms import CrispyFormMixin, ConfirmForm
from apps.account.forms import SignupInnerForm
from crispy_forms import layout
from django.core.exceptions import ValidationError
from django.forms.widgets import HiddenInput


class DriverJobRequestForm(CrispyFormMixin, forms.ModelForm):
    """Form for submitting a job request.
    Should be instantiated with a Client object.
    """
    submit_text = 'Book'
    submit_context = {'icon_name': 'driverjobrequest_create'}
#     def __init__(self, *args, **kwargs):
#         self.client = kwargs.pop('client')
#
#         super(DriverJobRequestForm, self).__init__(*args, **kwargs)
#
#         self.fields['client'].widget = HiddenInput()
#         self.fields['client'].initial = self.client

    def save(self, client, commit=True):
        """We require the client to be passed at save time.  This is
        to make it easier to include the form before the client is created,
        such as in the anonymous creation of bookings."""
        # Make sure the client is saved in the job request
        self.instance.client = client
        return super(DriverJobRequestForm, self).save(commit)

    class Meta:
        model = DriverJobRequest
        exclude = ('client', 'status')


class DriverJobRequestInnerForm(DriverJobRequestForm):
    """DriverJobRequestForm for including with other forms in a
    single html <form>.
    """
    form_tag = False
    submit_name = None
    wrap_fieldset_title = 'Job details'


class DriverJobRequestSignupInnerForm(SignupInnerForm):
    submit_name = 'book'
    submit_text = 'Book a driver'
    submit_context = {'icon_name': 'book'}

    def __init__(self, *args, **kwargs):
        super(DriverJobRequestSignupInnerForm, self).__init__(*args, **kwargs)

        self.helper.layout[0].insert(0, layout.HTML(
            """<p>Already have an account on Buzzhire?
            Please <a href='{% url 'account_login' %}'>log in</a>, or 
            if you forgot your password you can
            <a href='{% url 'account_reset_password' %}'>reset it</a>.</p>"""))

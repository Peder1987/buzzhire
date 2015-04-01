from django import forms
from django.forms import widgets
from .models import DriverJobRequest
from apps.core.forms import CrispyFormMixin, ConfirmForm
from apps.account.forms import SignupInnerForm
from crispy_forms import layout
from django.core.exceptions import ValidationError
from django.forms.widgets import HiddenInput
from apps.core.widgets import Bootstrap3SterlingMoneyWidget
from django.forms import widgets

class DriverJobRequestForm(CrispyFormMixin, forms.ModelForm):
    """Form for submitting a job request.
    Should be instantiated with a Client object.
    """
    submit_text = 'Book'
    submit_context = {'icon_name': 'driverjobrequest_create'}

    def __init__(self, *args, **kwargs):
        super(DriverJobRequestForm, self).__init__(*args, **kwargs)

        amount, currency = self.fields['pay_per_hour'].fields
        self.fields['pay_per_hour'].widget = Bootstrap3SterlingMoneyWidget(
           amount_widget=amount.widget, currency_widget=widgets.HiddenInput)


    def save(self, client, commit=True):
        """We require the client to be passed at save time.  This is
        to make it easier to include the form before the client is created,
        such as in the anonymous creation of bookings."""
        # Make sure the client is saved in the job request
        self.instance.client = client
        return super(DriverJobRequestForm, self).save(commit)

    class Meta:
        model = DriverJobRequest
        fields = ('date', 'start_time', 'duration', 'pay_per_hour',
                  'vehicle_types', 'driving_experience',
                  'number_of_freelancers')


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
            """<p>Please give us an email address and password that you
            can use to sign in to the site."""))

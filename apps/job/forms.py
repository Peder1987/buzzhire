from decimal import Decimal
from django import forms
from django.forms import widgets
from django.conf import settings
from .models import DriverJobRequest
from apps.core.forms import CrispyFormMixin, ConfirmForm
from apps.account.forms import SignupInnerForm
from django.template.loader import render_to_string
from apps.core.email import send_mail
from crispy_forms import layout
from django.core.exceptions import ValidationError
from apps.core.widgets import IndividualAttrsRadioSelect
from django.forms.widgets import HiddenInput
from apps.core.widgets import Bootstrap3SterlingMoneyWidget, Bootstrap3TextInput
from django.forms import widgets
from apps.location.forms import PostcodeFormMixin
from apps.payment.utils import PaymentAPI, PaymentException
import logging
from __builtin__ import True


logger = logging.getLogger('project')


class DriverJobRequestForm(CrispyFormMixin, PostcodeFormMixin,
                           forms.ModelForm):
    """Form for submitting a job request.
    Should be instantiated with a Client object.
    """
    submit_text = 'Book'
    submit_context = {'icon_name': 'driverjobrequest_create'}
    postcode_required = True

    def __init__(self, *args, **kwargs):
        if 'data' in kwargs:
            # If the form has been submitted, add the disabled city widget
            # value to the data before continuing.  This is because otherwise,
            # if the form fails validation then it doesn't show anything in the
            # city widget the second time.
            data = kwargs['data'].copy()
            # The posted key is different if the form has a prefix
            self.prefix = kwargs.get('prefix')
            data[self.add_prefix('city')] = DriverJobRequest.CITY_LONDON
            kwargs['data'] = data
        super(DriverJobRequestForm, self).__init__(*args, **kwargs)

        amount, currency = self.fields['client_pay_per_hour'].fields
        self.fields['client_pay_per_hour'].widget = Bootstrap3SterlingMoneyWidget(
          amount_widget=widgets.NumberInput(
                                    attrs={'min': settings.CLIENT_MIN_WAGE}),
          currency_widget=widgets.HiddenInput,
          attrs={'step': '0.25'})
        self.fields['start_time'].widget = forms.TimeInput()
        self.fields['duration'].widget = Bootstrap3TextInput(addon_after='hours')
        self.fields['city'].widget.attrs = {'disabled': 'disabled'}

        # Adjust display of radios
        self.fields['vehicle_type'].empty_label = 'Any'
        self.fields['vehicle_type'].initial = ''  # Set 'Any' radio as default

        self.fields['comments'].widget.attrs = {'rows': 3}
        self.helper.layout = layout.Layout(
            layout.Fieldset('Date and time',
                'date', 'start_time', 'duration',
            ),
            layout.Fieldset('Location',
                'address1', 'address2',
                'city',
                'raw_postcode',
            ),
            layout.Fieldset('Vehicle',
                layout.Div('vehicle_type', css_class="radios-wrapper"),
                'own_vehicle',
                'minimum_delivery_box',
            ),
            layout.Fieldset('Driver details',
                'number_of_freelancers',
                'driving_experience',
                'phone_requirement',
            ),
            layout.Fieldset('Budget',
                'client_pay_per_hour',
                'tips_included',
            ),
            layout.Fieldset('Further info',
                'comments'
            ),
        )

        # Add the submit button, but allow subclassing forms to suppress it
        if self.submit_name:
            self.helper.layout.append(self.get_submit_button())

    def save(self, client, commit=True):
        """We require the client to be passed at save time.  This is
        to make it easier to include the form before the client is created,
        such as in the anonymous creation of bookings."""
        # Make sure the client is saved in the job request
        self.instance.client = client
        # Make sure the city of London is saved
        # self.instance.city = DriverJobRequest.CITY_LONDON
        self.instance.postcode = self.cleaned_data['postcode']
        return super(DriverJobRequestForm, self).save(commit)

    class Meta:
        model = DriverJobRequest
        fields = ('date', 'start_time', 'duration',
                  'address1', 'address2', 'city',
                  'client_pay_per_hour', 'tips_included',
                  'vehicle_type', 'own_vehicle',
                  'minimum_delivery_box',
                  'driving_experience',
                  'number_of_freelancers',
                  'phone_requirement',
                  'comments')
        widgets = {
            'vehicle_type': IndividualAttrsRadioSelect(
                                                individual_attrs={'hello'}),
        }


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

class DriverJobRequestUpdateForm(DriverJobRequestForm):
    "Edit form for driver job requests."
    submit_text = 'Save'
    submit_context = {}

    notify = forms.BooleanField(
            label='Notify the client when saving this job.',
            required=False, initial=True)

    def __init__(self, *args, **kwargs):
        super(DriverJobRequestUpdateForm, self).__init__(*args, **kwargs)
        self.helper.layout.insert(-1,
            layout.Fieldset('Notifications', 'notify')
        )

    def save(self, *args, **kwargs):
        kwargs['client'] = self.instance.client
        instance = super(DriverJobRequestUpdateForm, self).save(*args, **kwargs)
        if self.cleaned_data['notify']:
            # Notify the client
            content = render_to_string(
                'job/email/includes/driverjobrequest_changed.html',
                {'object': instance})
            send_mail(instance.client.user.email,
                  'Your job request has been changed',
                  'email/base',
                  {'title':
                   'Your job request has been changed',
                   'content': content,
                   'bookings_email': settings.BOOKINGS_EMAIL},
                  from_email=settings.BOOKINGS_EMAIL)
        return instance



class JobRequestCheckoutForm(CrispyFormMixin, forms.Form):
    submit_text = 'Confirm and pay'
    submit_context = {'icon_name': 'pay'}
    submit_template_name = 'payment/forms/buttons.html'

    # This is the hidden field that the Braintree drop in UI fills out,
    # which allows us to take the payment.
    payment_method_nonce = forms.CharField(required=True,
                                           widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance')
        super(JobRequestCheckoutForm, self).__init__(*args, **kwargs)
        self.helper.layout.insert(0, layout.Div(
                                        css_id='payment-method-container'))

    def clean(self):
        cleaned_data = super(JobRequestCheckoutForm, self).clean()
        # Check everything else is valid before attempting payment
        if self.is_valid():
            # Attempt payment
            try:
                api = PaymentAPI()
                api.take_payment(self.cleaned_data['payment_method_nonce'],
                                 amount=self.instance.client_total_cost.amount,
                                 order_id=self.instance.reference_number)

            except PaymentException as e:
                logger.exception(e)
                raise forms.ValidationError(
                                   'Sorry, there was an issue taking payment.')

    def save(self):
        # Payment will have been successfully processed
        self.instance.open()
        self.instance.save()

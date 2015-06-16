import calendar
from decimal import Decimal
from django import forms
from django.forms import widgets
from django.db.models import BooleanField, Q
from apps.core.forms import CrispyFormMixin
from multiselectfield.forms.fields import MultiSelectFormField
from djmoney.forms.fields import MoneyField
from apps.core.widgets import Bootstrap3SterlingMoneyWidget
from .models import Availability, Booking
from apps.freelancer.models import client_to_freelancer_rate, Freelancer
from apps.job.models import JobRequest
from apps.driver.models import Driver, VehicleType, DriverVehicleType, \
                                            FlexibleVehicleType
from apps.location.forms import PostcodeFormMixin
from apps.core.forms import ConfirmForm
from django.contrib.gis.measure import D
from .utils import JobMatcher


class AvailabilityForm(forms.ModelForm):
    "Form for a freelancer to edit their availability."
    submit_text = 'Update availability'

    def __init__(self, *args, **kwargs):
        super(AvailabilityForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            if isinstance(Availability._meta.get_field(field_name),
                          BooleanField):
                self.fields[field_name].widget = forms.Select(
                                    choices=Availability.AVAILABILITY_CHOICES)


    def get_field_table(self):
        """Returns the form fields in the format suitable for arranging
        into a table, helpful for templates to iterate over:
        
            {
                'headings': ('Early morning (2am - 7am)',
                             'Morning (7am - 12pm)', ...),
                'rows': [
                    {
                        'heading': 'Monday',
                        'fields': (<form field>, <form field>, ...)
                    },
                    {
                        'heading': 'Tuesday',
                        'fields': (<form field>, <form field>, ...)
                    },
                    ...
                ]
            }
        """
        table = {
            'headings': None,
            'rows': [],
        }
        for day in Availability.DAYS:
            fields = [self['%s_%s' % (day, shift)]
                                        for shift in Availability.SHIFTS]
            row = {
                'heading': day.capitalize(),
                'fields': fields,
            }
            table['rows'].append(row)
            if table['headings'] is None:
                table['headings'] = [f.help_text for f in fields]
        return table

    class Meta:
        model = Availability
        exclude = ('freelancer',)


class JobMatchingForm(CrispyFormMixin, PostcodeFormMixin, forms.Form):
    """Form for searching drivers to help match them to jobs.
    Can be optionally instantiated with a job_request, which will prepopulate
    the search fields based on the job request's values.
    """

    date = forms.DateField(required=False)
    SHIFT_CHOICES = tuple([(None, '-- Enter shift --')] +
                          [(value, value.capitalize().replace('_', ' '))
                                for value in Availability.SHIFTS])
    shift = forms.ChoiceField(choices=SHIFT_CHOICES, required=False)

    vehicle_type = forms.ModelChoiceField(
                                queryset=FlexibleVehicleType.objects.all(),
                                required=False)
#     DRIVING_EXPERIENCE_CHOICES = (
#         (0, 'No preference'),
#         (1, '1 year'),
#         (3, '3 years'),
#         (5, '5 years'),
#     )

#     driving_experience = forms.ChoiceField(label='Minimum driving experience',
#                                     required=False,
#                                     choices=DRIVING_EXPERIENCE_CHOICES)

    client_pay_per_hour = MoneyField(max_digits=5, decimal_places=2,
                                     required=False)

    own_vehicle = forms.BooleanField(
                                label='The driver needs their own vehicle.',
                                required=False)
    minimum_delivery_box = forms.ChoiceField(required=False,
                        choices=DriverVehicleType.DELIVERY_BOX_CHOICES,
                        help_text='N.B. This will filter out any vehicle '
                            'that does not have a delivery box of at least '
                            'this size, including cars.')

    phone_requirement = forms.ChoiceField(required=False,
                                choices=JobRequest.PHONE_REQUIREMENT_CHOICES)

    # respect_travel_distance = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        # Set the job request, if it's provided
        self.job_request = kwargs.pop('job_request', None)
        super(JobMatchingForm, self).__init__(*args, **kwargs)
        amount, currency = self.fields['client_pay_per_hour'].fields
        self.fields['client_pay_per_hour'].widget = \
            Bootstrap3SterlingMoneyWidget(
               amount_widget=amount.widget,
               currency_widget=widgets.HiddenInput(attrs={'value': 'GBP'}),
               attrs={'step': '0.25'})

        if self.job_request:
            self.set_initial_based_on_job_request()

    def set_initial_based_on_job_request(self):
        "Sets the initial data based on the job request."
        matcher = JobMatcher(self.job_request)
        for name, value in matcher.search_terms.items():
            self.fields[name].initial = value

    def clean(self):
        super(JobMatchingForm, self).clean()
        # Ensure both, or neither, of the date / shift fields are set
        for full_field, empty_field in (('date', 'shift'), ('shift', 'date')):
            if self.cleaned_data.get(full_field) \
                                and not self.cleaned_data.get(empty_field):
                self.add_error(empty_field,
                       'If you are searching by %s, you '
                       'must also provide a %s.' % (full_field, empty_field))

    def get_results(self):
        """Returns the results of a successful search.
        Should be called after the form has been successfully validated."""
        matcher = JobMatcher(self.cleaned_data)
        results = matcher.get_results()
        # Also set the freelancer_pay_per_hour on the form
        self.freelancer_pay_per_hour = getattr(matcher,
                                            'freelancer_pay_per_hour', None)
        return results


class BookingOrInvitationConfirmForm(ConfirmForm):
    "Form for creating/editing a booking or invitation."
    inner_template_name = \
            'booking/includes/booking_or_invitation_confirm_form_inner.html'
    def __init__(self, *args, **kwargs):
        self.job_request = kwargs.pop('job_request')
        self.driver = kwargs.pop('driver')
        super(BookingOrInvitationConfirmForm, self).__init__(*args, **kwargs)


class InvitationAcceptForm(ConfirmForm):
    def __init__(self, *args, **kwargs):
        self.invitation = kwargs.pop('invitation')
        super(InvitationAcceptForm, self).__init__(*args, **kwargs)

    def save(self):
        # Create the booking
        return Booking.objects.create(jobrequest=self.invitation.jobrequest,
                               freelancer=self.invitation.freelancer)

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
from apps.driver.models import Driver, VehicleType, DriverVehicleType
from apps.location.forms import PostcodeFormMixin
from apps.core.forms import ConfirmForm
from django.contrib.gis.measure import D


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

    vehicle_types = forms.ModelMultipleChoiceField(
                                        queryset=VehicleType.objects.all(),
                                        required=False,
                                        widget=forms.CheckboxSelectMultiple)
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
        # Set initial for flat fields (i.e. ones that directly map between
        # form and job request attributes)
        FLAT_FIELDS = ('date', 'minimum_delivery_box', 'client_pay_per_hour',
                       'own_vehicle', 'phone_requirement')
        for field in FLAT_FIELDS:
            self.fields[field].initial = getattr(self.job_request, field)

        # Other fields
        self.fields['raw_postcode'].initial = str(self.job_request.postcode)
        self.fields['vehicle_types'].initial = \
                                        self.job_request.vehicle_types.all()

        self.fields['shift'].initial = Availability.shift_from_time(
                                                self.job_request.start_time)


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

        results = Driver.published_objects.all()

        results = self.filter_by_phone_requirement(results)
        results = self.filter_by_vehicle_requirements(results)
        results = self.filter_by_availability(results)
        results = self.filter_by_pay_per_hour(results)
        results = self.filter_by_location(results)

        # Return unique results
        return results.distinct()

    def filter_by_phone_requirement(self, results):
        "Filters by the phone requirement."
        PHONE_REQUIREMENT_MAP = {
            JobRequest.PHONE_REQUIREMENT_NOT_REQUIRED: lambda r: r,
            JobRequest.PHONE_REQUIREMENT_ANY:
                lambda r: r.exclude(
                    phone_type__in=(Freelancer.PHONE_TYPE_NON_SMARTPHONE, '')),
            JobRequest.PHONE_REQUIREMENT_ANDROID:
                lambda r: r.filter(phone_type=Freelancer.PHONE_TYPE_ANDROID),
            JobRequest.PHONE_REQUIREMENT_IPHONE:
                lambda r: r.filter(phone_type=Freelancer.PHONE_TYPE_IPHONE),
            JobRequest.PHONE_REQUIREMENT_WINDOWS:
                lambda r: r.filter(phone_type=Freelancer.PHONE_TYPE_WINDOWS),
        }

        if self.cleaned_data['phone_requirement']:
            results = PHONE_REQUIREMENT_MAP[
                            self.cleaned_data['phone_requirement']](results)
        return results

    def filter_by_vehicle_requirements(self, results):
        "Filters by vehicle requirements."

        if self.cleaned_data['vehicle_types']:
            if self.cleaned_data['own_vehicle']:
                # Filter by vehicle types that are owned
                filter_kwargs = {
                    'drivervehicletype__vehicle_type': \
                                    self.cleaned_data['vehicle_types'],
                    'drivervehicletype__own_vehicle': True
                }
                # Include delivery box filter, if specified
                if self.cleaned_data['minimum_delivery_box']:
                    filter_kwargs['drivervehicletype__delivery_box__gte'] = \
                                    self.cleaned_data['minimum_delivery_box']
                results = results.filter(**filter_kwargs)
            else:
                # Just filter by vehicle types
                filter_kwargs = {
                    'vehicle_types': self.cleaned_data['vehicle_types']
                }
            return results.filter(**filter_kwargs)

        return results

    def filter_by_availability(self, results):
        "Filters by availability, if it's been searched for."

        if self.cleaned_data['date']:

            # Get day of week for that date
            day_name = calendar.day_name[
                                self.cleaned_data['date'].weekday()].lower()

            # Build filter kwargs
            field_name = '%s_%s' % (day_name, self.cleaned_data['shift'])
            filter_kwargs = {'availability__%s' % field_name: True}

            # Filter
            results = results.filter(**filter_kwargs)

        return results

    def filter_by_pay_per_hour(self, results):
        """Filters the results based on the minimum pay per hour.
        """

        if self.cleaned_data['client_pay_per_hour']:
            self.freelancer_pay_per_hour = client_to_freelancer_rate(
                                    self.cleaned_data['client_pay_per_hour'])
            return results.filter(
                        minimum_pay_per_hour__lte=self.freelancer_pay_per_hour)
        return results

    def filter_by_location(self, results):
        """Filters the results by the supplied postcode, checking that it's
        within an acceptable distance for the driver."""
        if self.cleaned_data.get('postcode'):
            # Specific include distances so the template knows
            self.include_distances = True
            searched_point = self.cleaned_data['postcode'].point
            results = results.distance(searched_point,
                                       field_name='postcode__point')\
                        .order_by('distance')

            # if self.cleaned_data['respect_travel_distance']:
                # Filter by only those drivers whose travel distance works
                # with the postcode supplied
                # TODO - get this working with their personal distance settings
                # http://stackoverflow.com/questions/9547069/geodjango-distance-filter-with-distance-value-stored-within-model-query
                # results = results.filter(
                #      postcode__point__distance_lte=(searched_point, D(mi=4)))

        return results


class BookingConfirmForm(ConfirmForm):
    "Form for creating/editing a booking."
    inner_template_name = 'booking/includes/booking_confirm_form_inner.html'
    def __init__(self, *args, **kwargs):
        self.job_request = kwargs.pop('job_request')
        self.driver = kwargs.pop('driver')
        super(BookingConfirmForm, self).__init__(*args, **kwargs)
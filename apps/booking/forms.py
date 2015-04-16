import calendar
from decimal import Decimal
from django import forms
from django.forms import widgets
from django.db.models import BooleanField
from apps.core.forms import CrispyFormMixin
from multiselectfield.forms.fields import MultiSelectFormField
from djmoney.forms.fields import MoneyField
from apps.core.widgets import Bootstrap3SterlingMoneyWidget
from .models import Availability
from apps.driver.models import Driver, VehicleType, DriverVehicleType


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


class JobMatchingForm(CrispyFormMixin, forms.Form):
    """Form for searching drivers to help match them to jobs."""

    date = forms.DateField(required=False)
    SHIFT_CHOICES = tuple([(None, '-- Enter shift --')] +
                          [(value, value.capitalize().replace('_', ' '))
                           for value in Availability.SHIFTS])
    shift = forms.ChoiceField(choices=SHIFT_CHOICES, required=False)

    vehicle_types = forms.ModelMultipleChoiceField(
                                        queryset=VehicleType.objects.all(),
                                        required=False,
                                        widget=forms.CheckboxSelectMultiple)
    DRIVING_EXPERIENCE_CHOICES = (
        (0, 'No preference'),
        (1, '1 year'),
        (3, '3 years'),
        (5, '5 years'),
    )

    minimum_driving_experience = forms.ChoiceField(required=False,
                                    choices=DRIVING_EXPERIENCE_CHOICES)

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
    PHONE_TYPE_CHOICES = ((None, 'No preference'),) \
                         + Driver.PHONE_TYPE_CHOICES
    phone_type = forms.ChoiceField(required=False,
                                   choices=PHONE_TYPE_CHOICES)

    # Maps field name to filter kwargs when searching
    FILTER_MAP = {
        'minimum_driving_experience': 'driving_experience__gte',
        'phone_type': 'phone_type',
    }

    def __init__(self, *args, **kwargs):
        super(JobMatchingForm, self).__init__(*args, **kwargs)
        amount, currency = self.fields['client_pay_per_hour'].fields
        self.fields['client_pay_per_hour'].widget = \
            Bootstrap3SterlingMoneyWidget(
               amount_widget=amount.widget,
               currency_widget=widgets.HiddenInput(attrs={'value': 'GBP'}),
               attrs={'step': '0.25'})

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

        results = self.filter_from_map(results)

        results = self.filter_by_vehicle_requirements(results)
        results = self.filter_by_availability(results)

        # Return unique results
        return results.distinct()

    def filter_from_map(self, results):
        """Filters the results based on the FILTER_MAP that is used
        to define the behaviour for most of the fields."""
        filter_kwargs = {}
        for field_name, filter_kwarg in self.FILTER_MAP.items():
            if self.cleaned_data[field_name]:
                filter_kwargs[filter_kwarg] = self.cleaned_data[field_name]
        return results.filter(**filter_kwargs)

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

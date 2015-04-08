from django import forms
from django.db.models import BooleanField
from apps.core.forms import CrispyFormMixin
from multiselectfield.forms.fields import MultiSelectFormField
from .models import Availability
from apps.driver.models import Driver


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

    # NB the MultiSelectFormField doesn't work properly with searching;
    # we'll probably need to switch it to a manytomanyfield
    vehicle_types = MultiSelectFormField(choices=Driver.VEHICLE_TYPE_CHOICES,
                                         required=False)
    DRIVING_EXPERIENCE_CHOICES = (
        (0, 'No preference'),
        (1, '1 year'),
        (3, '3 years'),
        (5, '5 years'),
    )

    minimum_driving_experience = forms.ChoiceField(required=False,
                                    choices=DRIVING_EXPERIENCE_CHOICES)
    own_vehicle = forms.BooleanField(label='The driver needs their own vehicle.',
                                     required=False)

#     available_time_period = forms.ChoiceField(label='',
#                                choices=AvailableSlot.TIME_PERIOD_CHOICES,
#                                initial=AvailableSlot.TIME_PERIOD_ALLDAY)
#
#     specialism = forms.ModelChoiceField(queryset=None, required=False)
#     qualification_level = forms.ModelChoiceField(queryset=None, required=False)
#     skills = forms.ModelChoiceField(queryset=None, required=False)
#     languages = forms.ModelChoiceField(queryset=None, required=False)

    # Maps field name to filter kwargs when searching
    FILTER_MAP = {
        'vehicle_types': 'vehicle_types',
        'minimum_driving_experience': 'driving_experience__gte',
    }

    def __init__(self, *args, **kwargs):
        super(JobMatchingForm, self).__init__(*args, **kwargs)
        # self.helper.form_method = 'GET'

    def get_results(self):
        """Returns the results of a successful search.
        Should be called after the form has been successfully validated."""

        results = Driver.published_objects.all()

        results = self.filter_from_map(results)

        # results = self.filter_by_driving_experience(results)
        results = self.filter_by_own_vehicle(results)
        # results = self.filter_by_availability(results)

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

    def filter_by_driving_experience(self, results):
        "Filters by driving experience, if it's been searched for."

        if self.cleaned_data['minimum_driving_experience']:
            # TODO - should probably change way driving experience is stored
            # in the database, so we can do 'greater than' queries
            pass
        return results


    def filter_by_own_vehicle(self, results):
        "Filters by own vehicle, if it's been required."

        if self.cleaned_data['own_vehicle']:
            results = results.filter(own_vehicle=True)
        return results

    def filter_by_availability(self, results):
        "Filters by availability, if it's been searched for."

        if self.cleaned_data['available_date']:

            # Build filter kwargs for the date
            filter_kwargs = {'user__available_slots__date':
                                        self.cleaned_data['available_date']}

            # Build filter kwargs for the time period
            if self.cleaned_data['available_time_period'] == \
                                            AvailableSlot.TIME_PERIOD_ALLDAY:
                # If they're just searching for all day availability,
                # we it's a straightforward search for slots with that choice
                filter_kwargs['user__available_slots__time_period'] = \
                                            AvailableSlot.TIME_PERIOD_ALLDAY
            else:
                # If it's AM/PM, we search for slots with that choice,
                # OR all day
                filter_kwargs['user__available_slots__time_period__in'] = (
                     self.cleaned_data['available_time_period'],
                     AvailableSlot.TIME_PERIOD_ALLDAY
                )

            # Filter
            results = results.filter(**filter_kwargs)

        return results

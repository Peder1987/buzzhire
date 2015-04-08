from django import forms
from django.db.models import BooleanField
from apps.core.forms import CrispyFormMixin
from .models import Availability


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


from django import forms
from django.forms import widgets
from .models import JobRequest
from apps.core.forms import CrispyFormMixin, ConfirmForm
from crispy_forms import layout
from .templatetags.job import jobrequest_status_color, jobrequest_status_icon
from django.core.exceptions import ValidationError
from django.forms.widgets import HiddenInput


class JobRequestForm(CrispyFormMixin, forms.ModelForm):
    """Form for submitting a job request.
    Should be instantiated with a client EmailUser object.
    """
    def __init__(self, *args, **kwargs):
        self.client = kwargs.pop('client')

        super(JobRequestForm, self).__init__(*args, **kwargs)

        self.fields['client'].widget = HiddenInput()
        self.fields['client'].initial = self.client

        self.helper.layout = layout.Layout(

            layout.Fieldset('Location and date',
                'location_address',
                'regularity_type',
                'client',
                layout.Div(
                    'job_date',
                    'job_time',
                    css_id='regularity-type-one-off',
                    css_class='regularity-type-fields',
                ),
                layout.Div(
                    'regular_booking_details',
                    css_id='regularity-type-regular',
                    css_class='regularity-type-fields',
                ),
                'interpreting_method',
            ),
            layout.Fieldset('Support details',
                'provider_gender',
                'skill',
                'qualification_level',
                'language',
                'specialism',
                'number_of_providers',
            ),
            layout.Fieldset('Job overview and payment details',
                'budget',
                'payment_method',
                'atw_letter',
                'overview',
            ),
            layout.Submit('submit', 'Submit job request'),
        )

    def clean(self):
        cleaned_data = super(JobRequestForm, self).clean()
        # Simulate required fields for regularity fields
        required_message = 'This field is required.'
        if cleaned_data.get('regularity_type') == \
                                            JobRequest.REGULARITY_TYPE_REGULAR:
            if not cleaned_data.get('regular_booking_details'):
                self.add_error('regular_booking_details', required_message)
        else:
            # It's a one off booking
            for field_name in ('job_date', 'job_time'):
                if not cleaned_data.get(field_name):
                    self.add_error(field_name, required_message)

    def save(self, commit=True):
        # Make sure the client is saved in the job request
        self.instance.client = self.client
        return super(JobRequestForm, self).save(commit)

    class Meta:
        model = JobRequest
        exclude = 'status',
        widgets = {
            'location_address': widgets.Textarea(attrs={'rows': 3}),
            'overview': widgets.Textarea(attrs={'rows': 3}),
            'other_information': widgets.Textarea(attrs={'rows': 3}),
        }


class JobRequestConfirmActionForm(ConfirmForm):
    "Form for confirming an action on a job request."

    cancel_text = "Don't confirm yet"

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance')
        self.status = kwargs.pop('status')
        super(JobRequestConfirmActionForm, self).__init__(*args, **kwargs)

    def get_confirm_button(self):
        color = jobrequest_status_color(self.status)
        icon = jobrequest_status_icon(self.status)
        return layout.HTML(
            "<button class='btn btn-%s'>%s %s</button>" % (color, icon,
                                                           self.action_text))
    def clean(self):
        cleaned_data = super(JobRequestConfirmActionForm, self).clean()
        # Do not allow job requests to be completed if they do not have a fee
        if self.status == JobRequest.STATUS_OPEN \
                                        and not self.instance.provider_fee:
            raise ValidationError(
                    'You must enter a fee before opening this job request.')

    def save(self):
        "Triggered automatically when using this in an UpdateView."
        self.instance.update_status(self.status)
        return self.instance

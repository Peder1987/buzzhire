from django import forms
from apps.account.forms import SignupForm as BaseSignupForm
from crispy_forms.helper import FormHelper
from crispy_forms import layout
from .models import Driver


class SignupForm(BaseSignupForm):
    """This sign up form is included with SignupFormDriverDetails in
    the same html <form>.
    
    It's the same as the standard SignupForm but with the <form>
    and submit buttons removed. 
    """
    form_tag = False
    submit_name = None


class SignupFormDriverDetails(forms.ModelForm):
    """A form for filling out driver details, included with SignupForm in
    a single html <form>.
    """
    def __init__(self, *args, **kwargs):
        super(SignupFormDriverDetails, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False

        self.helper.layout = layout.Layout(
            layout.Fieldset(
                'Contact details',
                'first_name',
                'last_name',
                'mobile',
            ),
            layout.Fieldset(
                'About you',
                'english_fluency',
                'eligible_to_work',
                'vehicle_types',
                'driving_experience',
                'motorcycle_licence',
            ),
            layout.Fieldset(
                'Your equipment',
                'phone_type',
                'own_vehicle',
            ),
            layout.Fieldset(
                'Your availability',
                'days_available',
                'hours_available',
            ),
        )

        self.helper.layout.append(layout.Submit('submit', 'Sign up'))

    def save(self, user):
        "Saves the driver model, given the user."
        self.instance.user = user
        return super(SignupFormDriverDetails, self).save()

    class Meta:
        model = Driver
        exclude = ('user',)


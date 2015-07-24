from django import forms
from django.forms import widgets
from crispy_forms import layout
from apps.core.forms import CrispyFormMixin
from apps.location.forms import PostcodeFormMixin
from .models import Freelancer, FREELANCER_MIN_WAGE
from apps.core.widgets import Bootstrap3SterlingMoneyWidget


class PhotoUploadForm(CrispyFormMixin, forms.ModelForm):
    "Form for uploading a photo."
    submit_text = 'Upload'
    submit_context = {'icon_name': 'upload'}

    def __init__(self, *args, **kwargs):
        super(PhotoUploadForm, self).__init__(*args, **kwargs)
        self.fields['photo'].required = True

    class Meta:
        model = Freelancer
        fields = ('photo',)
        widgets = {
            'photo': widgets.FileInput
        }


class SignupFormFreelancerDetailsMixin(object):
    """Form mixin, used to create a form for filling out freelancer details,
    included with SignupForm in a single html <form>.
    Should be mixed in with a model form for the relevant Freelancer model.
    """
    form_tag = False
    submit_text = 'Sign up'
    submit_context = {'icon_name': 'login'}

    def save(self, user):
        "Saves the freelancer model, given the user."
        self.instance.user = user
        return super(SignupFormFreelancerDetailsMixin, self).save()



class FreelancerForm(CrispyFormMixin, PostcodeFormMixin, forms.ModelForm):
    """Edit form for a freelancer's profile."""
    submit_text = 'Save profile'
    submit_context = {'icon_name': 'edit'}


    def __init__(self, *args, **kwargs):
        super(FreelancerForm, self).__init__(*args, **kwargs)

        amount, currency = self.fields['minimum_pay_per_hour'].fields
        self.fields['minimum_pay_per_hour'].widget = \
            Bootstrap3SterlingMoneyWidget(
              amount_widget=widgets.NumberInput(
                                        attrs={'min': FREELANCER_MIN_WAGE}),
              currency_widget=widgets.HiddenInput,
              attrs={'step': '0.25'}
            )

        self.fields['raw_postcode'].help_text = 'The postcode of where you ' \
                'are based. This helps us match you with jobs that are nearby.'

        # Prepopulate raw_postcode field if there is already a postcode
        if self.instance.postcode:
            self.fields['raw_postcode'].initial = str(self.instance.postcode)

        self.fields['first_name'].label = False

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
                'years_experience',
            ),
            layout.Fieldset(
                'Your rates',
                'minimum_pay_per_hour',
            ),
            layout.Fieldset(
                'Your location',
                'raw_postcode',
                'travel_distance',
            ),
        )

        self.helper.layout.append(self.get_submit_button())

    class Meta:
        model = Freelancer
        exclude = ('user', 'published')
        widgets = {
            'years_experience': forms.widgets.Select,
        }
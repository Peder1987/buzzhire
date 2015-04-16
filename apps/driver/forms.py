from django import forms
from apps.core.forms import CrispyFormMixin
from crispy_forms.helper import FormHelper
from crispy_forms import layout
from .models import Driver, DriverVehicleType, VehicleType


class DriverForm(CrispyFormMixin, forms.ModelForm):
    """Edit form for a driver's profile."""
    submit_text = 'Save profile'
    submit_context = {'icon_name': 'edit'}

    def __init__(self, *args, **kwargs):
        super(DriverForm, self).__init__(*args, **kwargs)

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
                'driving_experience',
                'motorcycle_licence',
            ),
            layout.Fieldset(
                'Your equipment',
                'phone_type',
                'delivery_box',
            ),
#             layout.Fieldset(
#                 'Your availability',
#                 'days_available',
#                 'hours_available',
#             ),
        )

        self.helper.layout.append(self.get_submit_button())

    class Meta:
        model = Driver
        exclude = ('user', 'vehicle_types')
        widgets = {
            'driving_experience': forms.widgets.Select,
        }


class SignupFormDriverDetails(DriverForm):
    """A form for filling out driver details, included with SignupForm in
    a single html <form>.
    """
    form_tag = False
    submit_text = 'Sign up'
    submit_context = {'icon_name': 'login'}

    def save(self, user):
        "Saves the driver model, given the user."
        self.instance.user = user
        return super(SignupFormDriverDetails, self).save()


class DriverVehicleTypeForm(CrispyFormMixin, forms.ModelForm):
    "Form for creating/editing a driver vehicle."

    @property
    def submit_text(self):
        return 'Save' if self.instance.pk else 'Create'

    @property
    def submit_context(self):
        icon_name = 'save' if self.instance.pk else 'create'
        return {'icon_name': icon_name}


    def __init__(self, *args, **kwargs):
        self.driver = kwargs.pop('driver')
        super(DriverVehicleTypeForm, self).__init__(*args, **kwargs)

        # Limit choices to vehicle types they haven't already created
        existing_vehicle_types = self.driver.vehicle_types.values('pk')
        if self.instance.pk:
            # If we're editing it, we should include the object's own vehicle
            existing_vehicle_types = existing_vehicle_types.exclude(
                                            pk=self.instance.vehicle_type.pk)
        self.fields['vehicle_type'].queryset = VehicleType.objects.exclude(
                                            pk__in=existing_vehicle_types)

    def save(self):
        self.instance.driver = self.driver
        return super(DriverVehicleTypeForm, self).save()

    class Meta:
        model = DriverVehicleType
        fields = ('vehicle_type', 'own_vehicle', 'delivery_box')

from django import forms
from django.forms import widgets
from django.core.exceptions import ValidationError
from apps.core.forms import CrispyFormMixin
from crispy_forms.helper import FormHelper
from .models import Driver, DriverJobRequest, DriverVehicleType, VehicleType
from apps.job.forms import JobRequestForm, JobRequestUpdateMixin
from apps.core.widgets import ChoiceAttrsRadioSelect
from apps.freelancer.forms import FreelancerForm


class DriverJobRequestForm(JobRequestForm):
    """Form for creating/editing driver job requests.
    """

    def __init__(self, *args, **kwargs):
        super(DriverJobRequestForm, self).__init__(*args, **kwargs)
        self.adjust_vehicle_type_widget()
        self.helper.layout.insert(3,
            layout.Fieldset('Vehicle',
                layout.Div('vehicle_type', css_class="radios-wrapper"),
                'own_vehicle',
                'minimum_delivery_box',
            )
        )
        self.helper.layout[2].insert(1, 'driving_experience')

    def adjust_vehicle_type_widget(self):
        """Adjusts the vehicle type widget so it has
        'data-delivery-box_applicable' set on any radios that need a delivery
        box.  The javascript will use this to hide/show the delivery box field. 
        """
        # Adjust display of radios
        self.fields['vehicle_type'].empty_label = 'Any'
        self.fields['vehicle_type'].initial = ''  # Set 'Any' radio as default

        # Build list of the vehicle types that need a delivery box
        vehicle_type_choices = list(VehicleType.objects.filter(
                    delivery_box_applicable=True).values_list('pk', flat=True))
        vehicle_type_choices.append('')  # Also add the 'any' choice
        vehicle_type_attrs = dict(
            [(i, {'data-delivery-box-applicable': 'true'}) \
             for i in vehicle_type_choices])
        self.fields['vehicle_type'].widget = ChoiceAttrsRadioSelect(
                                choice_attrs=vehicle_type_attrs)

    class Meta(JobRequestForm.Meta):
         model = DriverJobRequest
         fields = JobRequestForm.Meta.fields + ('vehicle_type', 'own_vehicle',
                  'minimum_delivery_box', 'driving_experience')
         widgets = {
                'vehicle_type': ChoiceAttrsRadioSelect(),
         }


class DriverJobRequestUpdateForm(JobRequestUpdateMixin, DriverJobRequestForm):
    """Edit form for driver job requests."""
    # TODO - we can probably remove the need for this
    pass


class DriverForm(FreelancerForm):
    """Edit form for a driver's profile."""

    def __init__(self, *args, **kwargs):
        super(DriverForm, self).__init__(*args, **kwargs)
        self.helper.layout[1].append('driving_experience')

    class Meta(FreelancerForm.Meta):
        model = Driver
        exclude = FreelancerForm.Meta.exclude \
                        + ('vehicle_types', 'motorcycle_licence')
        widgets = {
            'driving_experience': forms.widgets.Select,
        }


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

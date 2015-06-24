from django import forms
from . import services


class ServiceSelectForm(forms.Form):
    """Form for selecting a service.
    """
    def __init__(self, *args, **kwargs):
        super(ServiceSelectForm, self).__init__(*args, **kwargs)
        # Populate the service field with each service
        service_choices = []
        for service in services.values():
            service_choices.append((service.key, service.title))
        self.fields['service'] = forms.ChoiceField(choices=service_choices)
        self.fields['service'].widget.attrs['class'] = 'form-control'

from django import forms
from apps.core.forms import CrispyFormMixin
from .models import Lead, Client
from crispy_forms.helper import FormHelper


class LeadForm(CrispyFormMixin, forms.ModelForm):
    """A form for filling out an expression of interest.
    """
    submit_text = 'Keep me posted'
    submit_context = {'icon_name': 'confirm'}
    class Meta:
        model = Lead
        exclude = ('created',)


class ClientForm(CrispyFormMixin, forms.ModelForm):
    """A form for editing client details.
    """
    submit_text = 'Save profile'
    submit_context = {'icon_name': 'edit'}

    class Meta:
        model = Client
        exclude = ('user',)
        widgets={
            "first_name":forms.TextInput(attrs={'placeholder':'First name'})
        }  


class ClientInnerForm(ClientForm):
    """A form for filling out client details, included with SignupForm in
    a single html <form>.
    """
    form_tag = False
    submit_text = 'Sign up'
    submit_context = {'icon_name': 'register'}
    wrap_fieldset_title = 'About you'

    def __init__(self, *args, **kwargs):
        super(ClientForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

    def save(self, user):
        "Saves the client model, given the user."
        self.instance.user = user
        return super(ClientForm, self).save()

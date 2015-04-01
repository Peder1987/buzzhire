from django import forms
from apps.core.forms import CrispyFormMixin
from .models import Lead, Client


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


class ClientInnerForm(ClientForm):
    """A form for filling out client details, included with SignupForm in
    a single html <form>.
    """
    form_tag = False
    submit_name = None
    wrap_fieldset_title = 'About you'

    def save(self, user):
        "Saves the client model, given the user."
        self.instance.user = user
        return super(ClientForm, self).save()

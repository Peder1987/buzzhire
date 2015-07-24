from allauth.account import forms
from apps.core.forms import CrispyFormMixin, ConfirmForm
from crispy_forms.helper import FormHelper

# Crispify all the allauth forms


class LoginForm(CrispyFormMixin, forms.LoginForm):
    submit_context = {'icon_name': 'login'}
    submit_text = 'Log in'


class LogoutForm(CrispyFormMixin, ConfirmForm):
    action_text = 'Logout'


class SignupForm(CrispyFormMixin, forms.SignupForm):
    submit_text = 'Sign up'


class SignupInnerForm(SignupForm):
    """This sign up form is the same as the standard SignupForm but with
    the <form> and submit buttons removed, used for including with other
    forms in a single html <form> tag. 
    """

    form_tag = False
    submit_name = None
    wrap_fieldset_title = ''

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False 
        self.fields['password2'].widget.attrs['placeholder'] = 'Password again'


class ResetPasswordForm(CrispyFormMixin, forms.ResetPasswordForm):
    submit_text = 'Reset'
    submit_context = {'icon_name': 'reset_password'}


class ResetPasswordKeyForm(CrispyFormMixin, forms.ResetPasswordKeyForm):
    submit_text = 'Save new password'
    submit_context = {'icon_name': 'password'}


class ChangePasswordForm(CrispyFormMixin, forms.ChangePasswordForm):
    submit_context = {'icon_name': 'password'}
    submit_text = 'Change password'

    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
       
        self.helper.form_show_labels = False
        self.helper.form_class = 'edit-password-form col-md-6'

from allauth.account import forms
from apps.core.forms import CrispyFormMixin, ConfirmForm

# Crispify all the allauth forms


class LoginForm(CrispyFormMixin, forms.LoginForm):
    submit_context = {'icon_name': 'login'}
    submit_text = 'Log in'


class LogoutForm(CrispyFormMixin, ConfirmForm):
    action_text = 'Logout'


class SignupForm(CrispyFormMixin, forms.SignupForm):
    submit_text = 'Sign up'


class ResetPasswordForm(CrispyFormMixin, forms.ResetPasswordForm):
    submit_text = 'Reset'
    submit_context = {'icon_name': 'reset_password'}


class ResetPasswordKeyForm(CrispyFormMixin, forms.ResetPasswordKeyForm):
    submit_text = 'Save new password'
    submit_context = {'icon_name': 'password'}


class ChangePasswordForm(CrispyFormMixin, forms.ChangePasswordForm):
    submit_context = {'icon_name': 'password'}
    submit_text = 'Change password'

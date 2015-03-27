from allauth.account import forms
from apps.core.forms import CrispyFormMixin, ConfirmForm

# Crispify all the allauth forms


class LoginForm(CrispyFormMixin, forms.LoginForm):
    pass


class LogoutForm(CrispyFormMixin, ConfirmForm):
    action_text = 'Logout'


class SignupForm(CrispyFormMixin, forms.SignupForm):
    submit_text = 'Sign up'


class ResetPasswordForm(CrispyFormMixin, forms.ResetPasswordForm):
    pass


class ResetPasswordKeyForm(CrispyFormMixin, forms.ResetPasswordKeyForm):
    pass


class ChangePasswordForm(CrispyFormMixin, forms.ChangePasswordForm):
    pass

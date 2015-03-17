from allauth.account import forms
from apps.core.forms import CrispyFormMixin


class LoginForm(CrispyFormMixin, forms.LoginForm):
    pass


class SignupForm(CrispyFormMixin, forms.SignupForm):
    pass


class ResetPasswordForm(CrispyFormMixin, forms.ResetPasswordForm):
    pass


class ResetPasswordKeyForm(CrispyFormMixin, forms.ResetPasswordKeyForm):
    pass

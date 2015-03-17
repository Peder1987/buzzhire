from allauth.account import views
from apps.core.views import ContextMixin
from . import forms


class SignupView(ContextMixin, views.SignupView):
    extra_context = {'title': 'Register'}
    form_class = forms.SignupForm


class LoginView(ContextMixin, views.LoginView):
    extra_context = {'title': 'Log in'}
    form_class = forms.LoginForm


class LogoutView(ContextMixin, views.LogoutView):
    extra_context = {'title': 'Log out'}
    template_name = 'form_page.html'


class PasswordResetView(ContextMixin, views.PasswordResetView):
    extra_context = {'title': 'Reset password'}
    form_class = forms.ResetPasswordForm


class PasswordResetDoneView(ContextMixin, views.PasswordResetDoneView):
    extra_context = {'title': 'Now check your email'}


class PasswordResetFromKeyView(ContextMixin, views.PasswordResetFromKeyView):
    extra_context = {'title': 'New password'}
    form_class = forms.ResetPasswordKeyForm


class PasswordResetFromKeyDoneView(ContextMixin,
                                   views.PasswordResetFromKeyDoneView):
    extra_context = {'title': 'Password reset complete'}

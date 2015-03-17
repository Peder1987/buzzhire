from allauth.account import views
from apps.core.views import ContextMixin, ConfirmationMixin
from . import forms
from django.core.urlresolvers import reverse_lazy


class SignupView(ContextMixin, views.SignupView):
    extra_context = {'title': 'Register'}
    form_class = forms.SignupForm


class LoginView(ContextMixin, views.LoginView):
    extra_context = {'title': 'Log in'}
    form_class = forms.LoginForm


class LogoutView(ContextMixin, ConfirmationMixin, views.LogoutView):
    extra_context = {'title': 'Log out'}
    question = 'Are you sure you want to log out?'
    cancel_url = reverse_lazy('index')


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


class PasswordChangeView(ContextMixin, views.PasswordChangeView):
    extra_context = {'title': 'Change password'}
    form_class = forms.ChangePasswordForm
    template_name = 'form_page.html'

class PasswordSetView(ContextMixin, views.PasswordSetView):
    extra_context = {'title': 'Password changed'}

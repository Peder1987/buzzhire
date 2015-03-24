from apps.account.views import SignupView as BaseSignupView
from allauth.account.utils import complete_signup
from allauth.account import app_settings
from . import forms


class SignupView(BaseSignupView):
    extra_context = {'title': 'Driver sign up'}
    form_class = forms.SignupForm
    template_name = 'driver/signup.html'
    # The form prefix for the account form
    prefix = 'account'

    def get_context_data(self, *args, **kwargs):
        context = super(SignupView, self).get_context_data(*args, **kwargs)
        context['driver_form'] = self.get_driver_form()

        return context

    def get_driver_form(self):
        return forms.SignupFormDriverDetails(**self.get_driver_form_kwargs())

    def get_driver_form_kwargs(self):
        """Standard get_form_kwargs() method adapted for the driver form."""

        kwargs = {
            'initial': self.get_initial(),
            'prefix': 'driver',
        }

        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def post(self, request, *args, **kwargs):
        "Standard post method adapted to validate both forms."
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        self.driver_form = self.get_driver_form()
        if form.is_valid() and self.driver_form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        'Adapted from BaseSignupView to save the driver too.'
        user = form.save(self.request)
        # Save driver form too
        self.driver_form.save(user)
        return complete_signup(self.request, user,
                               app_settings.EMAIL_VERIFICATION,
                               self.get_success_url())

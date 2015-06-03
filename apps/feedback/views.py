from django.views.generic.detail import SingleObjectMixin
from extra_views import FormSetView
from apps.client.views import OwnedByClientMixin
from apps.core.views import ContextMixin
from apps.job.models import JobRequest
from .models import BookingFeedback
from .forms import BookingFeedbackForm
from django.contrib import messages
from django.shortcuts import redirect


class ClientFeedbackAllowedMixin(object):
    """Views mixin - redirects to job request page, with an appropriate
    error message, if the client is not allowed to provide feedback on
    this job request.
    """
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()

        message = None
        if self.object.status != JobRequest.STATUS_COMPLETE:
            message = "You cannot leave feedback for a job that " \
                        "hasn't finished yet."
        elif BookingFeedback.objects.client_feedback_exists(self.object):
            message = 'You have already left feedback for this job.'
        if message:
            messages.error(self.request, message)
            return redirect(self.object.get_absolute_url())

        return super(ClientFeedbackAllowedMixin, self).dispatch(request,
                                                           *args, **kwargs)


class BookingFeedbackCreate(OwnedByClientMixin,
                            ClientFeedbackAllowedMixin,
                            ContextMixin, SingleObjectMixin,
                            FormSetView):
    """Page for a client to leave feedback on the freelancers
    for a particular job request.
    """
    template_name = 'feedback/feedback_create.html'
    extra_context = {'title': 'Leave feedback'}
    model = JobRequest
    extra = 0
    form_class = BookingFeedbackForm

    def get_initial(self):

        feedback_list = BookingFeedback.objects.feedback_list(self.object)
        # Convert to initial values
        initial = [BookingFeedbackForm.get_initial(feedback)
                   for feedback in feedback_list]
        return initial

    def formset_valid(self, formset):
        [form.save() for form in formset]
        messages.add_message(self.request, messages.INFO,
                             'Thanks for your feedback.')
        return super(BookingFeedbackCreate, self).formset_valid(formset)

    def get_success_url(self):
        return self.object.get_absolute_url()

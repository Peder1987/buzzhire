from django.views.generic.edit import CreateView, UpdateView
from apps.core.views import ContextMixin, TabsMixin, ConfirmationMixin
from django.core.urlresolvers import reverse_lazy
from .models import JobRequest
from django.views.generic.base import TemplateView
from .forms import JobRequestForm, JobRequestConfirmActionForm
from apps.provider.views import ProviderOnlyMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib import messages
from apps.account.views import AdminOnlyMixin
from apps.client.views import ClientOnlyMixin
from braces.views._access import AnonymousRequiredMixin
from django.shortcuts import redirect


class JobRequestList(ProviderOnlyMixin, ContextMixin, ListView):
    "Job listing page for LSPs."
    model = JobRequest
    paginate_by = 20
    extra_context = {'title': 'Job listings'}

    def get_queryset(self):
        return JobRequest.open_objects.all()


class JobRequestCreate(ContextMixin, CreateView):
    "Creation page for submitting a job request."
    extra_context = {'title': 'Create job request'}
    model = JobRequest
    success_url = reverse_lazy('jobrequest_complete')
    form_class = JobRequestForm

    def dispatch(self, request, *args, **kwargs):
        # if not logged in, redirect to a job request pre-sign up page
        if request.user.is_anonymous():
            return redirect('jobrequest_create_anon')
        return super(JobRequestCreate, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        form_kwargs = super(JobRequestCreate, self).get_form_kwargs()
        # Pass the logged in user as the client
        form_kwargs['client'] = self.request.user
        return form_kwargs


class JobRequestCreateAnonymous(AnonymousRequiredMixin,
                          ContextMixin, TemplateView):
    "Page for anonymous users who want to create a job request."
    template_name = 'job/jobrequest_create_anon.html'
    extra_context = {'title': 'Create job request'}


class JobRequestComplete(ClientOnlyMixin, ContextMixin, TemplateView):
    "Confirmation page on successful job request submission."
    template_name = 'job/complete.html'
    extra_context = {'title': 'Job confirmation'}


class JobRequestsModeration(AdminOnlyMixin, TabsMixin, ContextMixin, ListView):
    "Moderation view for job requests."
    model = JobRequest
    template_name = 'job/jobrequest_moderation.html'
    extra_context = {'title': 'Moderation'}
    paginate_by = 30
    tabs_query_component = 'status'

    def get_tabs(self):
        tabs = []
        for value, title in JobRequest.STATUS_CHOICES:
            tabs.append((title, '%s?status=%s' % (self.request.path, value)))
        return tabs

    def get_queryset(self):
        queryset = super(JobRequestsModeration, self).get_queryset()
        status = self.request.GET.get('status', JobRequest.STATUS_NEW)
        return queryset.filter(status=status)


class JobRequestDetail(ProviderOnlyMixin, DetailView):
    """Detail view of job requests, for admin and for providers."""
    model = JobRequest

    def get_template_names(self):
        # Use a custom template to show jobrequests that are not open
        # to non-admins
        if not self.request.user.is_admin and \
                                self.object.status != JobRequest.STATUS_OPEN:
            return ('job/jobrequest_detail_gone.html',)
        return ('job/jobrequest_detail.html',)

    def get_context_data(self, *args, **kwargs):
        context = super(JobRequestDetail, self).get_context_data(*args,
                                                                 **kwargs)
        context['title'] = self.object
        return context


class JobRequestConfirmAction(AdminOnlyMixin, ConfirmationMixin, UpdateView):
    "Confirmation page for different actions on JobRequests."

    form_class = JobRequestConfirmActionForm
    model = JobRequest
    template_name = 'job/jobrequest_confirm_action.html'
    status = None

    STATUS_MAP = {
        JobRequest.STATUS_OPEN: {
            'title': 'Open job request?',
            'question': 'Are you sure you want to open this job request? '
                        'This will publish it to the job listings page, '
                        'and notify the client.',
            'action_text': 'Open',
        },
        JobRequest.STATUS_FOLLOW_UP: {
            'title': 'Mark job request as needing follow up?',
            'question': 'Are you sure you want to mark this job request '
                        'as needing follow up?  This will move it to the '
                        '"Needs follow up" queue.',
            'action_text': 'Needs follow up',
        },
        JobRequest.STATUS_CANCELLED: {
            'title': 'Cancel job request?',
            'question': 'Are you sure you want to cancel this job request? '
                        'If you do, the client will be notified.',
            'action_text': 'Cancel',
        },
        JobRequest.STATUS_COMPLETE: {
            'title': 'Complete job request?',
            'question': 'Are you sure you want to complete this job request? '
                        'If you do, the client and any unsuccessful '
                        'applicants will be notified.',
            'action_text': 'Complete',
        },
    }

    def get_context_data(self, *args, **kwargs):
        context = super(JobRequestConfirmAction, self).get_context_data(*args,
                                                                    **kwargs)
        context['title'] = self.STATUS_MAP[self.status]['title']
        return context

    def get_form_kwargs(self):
        form_kwargs = super(JobRequestConfirmAction, self).get_form_kwargs()
        form_kwargs.update({
            'status':self.status,
            'action_text': self.STATUS_MAP[self.status]['action_text'],
            'cancel_text': 'Not yet',
        })
        return form_kwargs

    def get_question(self):
        return self.STATUS_MAP[self.status]['question']

    def get_cancel_url(self):
        # Go back to the job request page
        return self.object.get_absolute_url()

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS,
                             'Updated job request.')
        return self.object.get_absolute_url()

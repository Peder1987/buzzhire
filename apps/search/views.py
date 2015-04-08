from django.views.generic import ListView
from apps.account.views import AdminOnlyMixin
from apps.core.views import ContextMixin


class JobMatchingView(AdminOnlyMixin, ContextMixin, ListView):
    """View for searching drivers to match with jobs."""
    template_name = 'booking/job_matching.html'
    paginate_by = 100
    extra_context = {'title': 'Job matching'}

    def get(self, request, *args, **kwargs):
        # We use a form, but with the GET method as it's a search form.
        if self.request.GET.get('search', None):
            # A search has been made
            self.form = JobMatchingForm(self.request.GET)
        else:
            # No search made yet
            self.form = JobMatchingForm()
        return super(JobMatching, self).get(request, *args, **kwargs)

    def get_queryset(self):
        "Called first by get()."
        # Return the object_list, but only if the search form validates
        if self.form.is_valid():
            return self.form.get_results()
        return []

    def get_context_data(self, **kwargs):
        context = super(JobMatching, self).get_context_data(**kwargs)
        context['form'] = self.form

        if self.form.is_valid():
            # Set a searched flag to let the template know a search has run
            context['searched'] = True

        return context

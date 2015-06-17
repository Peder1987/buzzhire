from apps.job.forms import JobRequestUpdateMixin, JobRequestForm
from .models import ChefJobRequest


class ChefJobRequestForm(JobRequestForm):
    "General form for chef job requests."
    def __init__(self, *args, **kwargs):
        super(ChefJobRequestForm, self).__init__(*args, **kwargs)
        self.helper.layout[2].insert(1, 'certification')

    class Meta(JobRequestForm.Meta):
         model = ChefJobRequest
         fields = JobRequestForm.Meta.fields + ('certification',)


class ChefJobRequestUpdateForm(JobRequestUpdateMixin, ChefJobRequestForm):
    """Edit form for chef job requests."""
    pass

from django import forms
from apps.job.forms import JobRequestForm
from apps.freelancer.forms import FreelancerForm
from apps.booking.forms import JobMatchingForm
from .models import ChefJobRequest, Chef, CERTIFICATION_CHOICES
from .utils import ChefJobMatcher


class ChefJobRequestForm(JobRequestForm):
    "General form for chef job requests."
    def __init__(self, *args, **kwargs):
        super(ChefJobRequestForm, self).__init__(*args, **kwargs)
        self.helper.layout[2].insert(1, 'certification')

    class Meta(JobRequestForm.Meta):
         model = ChefJobRequest
         fields = JobRequestForm.Meta.fields + ('certification',)


class ChefForm(FreelancerForm):
    """Edit form for a chef's profile."""

    def __init__(self, *args, **kwargs):
        super(ChefForm, self).__init__(*args, **kwargs)
        self.helper.layout[1].append('certification')

    class Meta(FreelancerForm.Meta):
        model = Chef


class ChefJobMatchingForm(JobMatchingForm):
    """Job matching form specifically for chefs.
    """

    job_matcher = ChefJobMatcher
    certification = forms.ChoiceField(required=False,
                        choices=((None, '-------'),) + CERTIFICATION_CHOICES)

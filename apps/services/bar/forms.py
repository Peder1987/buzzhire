from django import forms
from apps.job.forms import JobRequestForm
from apps.freelancer.forms import FreelancerForm
from apps.booking.forms import JobMatchingForm
from .models import BarJobRequest, BarFreelancer



class BarJobRequestForm(JobRequestForm):
    "General form for bar staff job requests."

    class Meta(JobRequestForm.Meta):
         model = BarJobRequest


class BarFreelancerForm(FreelancerForm):
    """Edit form for a chef's profile."""

    class Meta(FreelancerForm.Meta):
        model = BarFreelancer

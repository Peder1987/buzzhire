from apps.job import services, Service
from .models import BarJobRequest, BarFreelancer
from .forms import BarJobRequestForm, BarFreelancerForm


class BarService(Service):
    "Class that defines the bar staff service."
    key = 'bar'

    job_request_model = BarJobRequest
    job_request_form = BarJobRequestForm

    freelancer_model = BarFreelancer
    freelancer_form = BarFreelancerForm


services.register(BarService)

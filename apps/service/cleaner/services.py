from apps.job import services, Service
from .models import CleanerJobRequest, Cleaner
from .forms import CleanerJobRequestForm, CleanerForm


class CleanerService(Service):
    "Class that defines the cleaner service."
    key = 'cleaner'

    job_request_model = CleanerJobRequest
    job_request_form = CleanerJobRequestForm

    freelancer_model = Cleaner
    freelancer_form = CleanerForm


services.register(CleanerService)

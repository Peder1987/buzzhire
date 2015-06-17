from apps.job import services, Service
from .models import ChefJobRequest
from .forms import ChefJobRequestUpdateForm


class ChefService(Service):
    "Class that defines the chef service."
    key = 'chef'
    job_request_model = ChefJobRequest
    job_request_edit_form = ChefJobRequestUpdateForm


services.register(ChefService)
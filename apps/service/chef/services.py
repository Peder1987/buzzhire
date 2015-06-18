from apps.job import services, Service
from .models import ChefJobRequest, Chef
from .forms import ChefJobRequestForm, ChefForm


class ChefService(Service):
    "Class that defines the chef service."
    key = 'chef'

    job_request_model = ChefJobRequest
    job_request_form = ChefJobRequestForm

    freelancer_model = Chef
    freelancer_form = ChefForm

services.register(ChefService)

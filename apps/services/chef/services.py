from apps.service import services, Service
from .models import ChefJobRequest, Chef
from .forms import ChefJobRequestForm, ChefForm, ChefJobMatchingForm


class ChefService(Service):
    "Class that defines the chef service."
    key = 'chef'

    job_request_model = ChefJobRequest
    job_request_form = ChefJobRequestForm

    freelancer_model = Chef
    freelancer_form = ChefForm

    job_matching_form = ChefJobMatchingForm

services.register(ChefService)

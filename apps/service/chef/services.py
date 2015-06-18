from apps.job import services, Service
from .models import ChefJobRequest, Chef
from .forms import ChefJobRequestForm, ChefJobRequestUpdateForm, ChefForm


class ChefService(Service):
    "Class that defines the chef service."
    key = 'chef'

    job_request_model = ChefJobRequest
    job_request_edit_form = ChefJobRequestUpdateForm
    job_request_create_form = ChefJobRequestForm

    freelancer_model = Chef
    freelancer_form = ChefForm

services.register(ChefService)

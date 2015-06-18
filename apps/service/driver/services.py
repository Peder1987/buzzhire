from apps.job import services, Service
from .models import DriverJobRequest, Driver
from .forms import DriverJobRequestForm, DriverJobRequestUpdateForm, DriverForm


class DriverService(Service):
    "Class that defines the driver service."
    key = 'driver'

    job_request_model = DriverJobRequest
    job_request_edit_form = DriverJobRequestUpdateForm
    job_request_create_form = DriverJobRequestForm

    freelancer_model = Driver
    freelancer_form = DriverForm

services.register(DriverService)

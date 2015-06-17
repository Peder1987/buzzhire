from apps.job import services, Service
from .models import DriverJobRequest
from .forms import DriverJobRequestForm, DriverJobRequestUpdateForm


class DriverService(Service):
    "Class that defines the driver service."
    key = 'driver'
    job_request_model = DriverJobRequest
    job_request_edit_form = DriverJobRequestUpdateForm
    job_request_create_form = DriverJobRequestForm


services.register(DriverService)

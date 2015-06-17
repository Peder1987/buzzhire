from apps.job import services, Service
from .models import DriverJobRequest
from .forms import DriverJobRequestUpdateForm


class DriverService(Service):
    "Class that defines the driver service."
    key = 'driver'
    job_request_model = DriverJobRequest
    job_request_edit_form = DriverJobRequestUpdateForm


services.register(DriverService)
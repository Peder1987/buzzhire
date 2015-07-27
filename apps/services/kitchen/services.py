from apps.service import services, Service
from .models import KitchenJobRequest, KitchenFreelancer
from .forms import (KitchenJobRequestForm, KitchenFreelancerForm,
                    KitchenJobMatchingForm)


class KitchenService(Service):
    "Class that defines the kitchen service."
    key = 'kitchen'
    weight = 5
    job_request_model = KitchenJobRequest
    job_request_form = KitchenJobRequestForm

    freelancer_model = KitchenFreelancer
    freelancer_form = KitchenFreelancerForm

    job_matching_form = KitchenJobMatchingForm

services.register(KitchenService)

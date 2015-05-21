from django.views.generic import CreateView
from .models import BookingFeedback
from .forms import BookingFeedbackForm


class BookingFeedbackCreate(CreateView):
    template_name = 'feedback/feedback_create.html'

    model = BookingFeedback
    form_class = BookingFeedbackForm

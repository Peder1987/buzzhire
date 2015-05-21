from django import forms
from apps.core.forms import CrispyFormMixin
from .models import BookingFeedback
from .widgets import RatingWidget


class BookingFeedbackForm(CrispyFormMixin,
                        forms.ModelForm):
    submit_text = 'Leave feedback'
    class Meta:
        model = BookingFeedback
        widgets = {
            'score': RatingWidget
        }

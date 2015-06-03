from django import forms
from django.forms import widgets
from apps.core.forms import CrispyFormMixin
from .models import Freelancer

class PhotoUploadForm(CrispyFormMixin, forms.ModelForm):
    "Form for uploading a photo."
    submit_text = 'Upload'
    submit_context = {'icon_name': 'upload'}

    def __init__(self, *args, **kwargs):
        super(PhotoUploadForm, self).__init__(*args, **kwargs)
        self.fields['photo'].required = True

    class Meta:
        model = Freelancer
        fields = ('photo',)
        widgets = {
            'photo': widgets.FileInput
        }

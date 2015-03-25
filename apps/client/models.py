from django.db import models
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField
from apps.freelancer.models import Freelancer


class Lead(models.Model):
    "A lead is an expression of interest created by a potential client."
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    more_information = models.TextField(
        help_text="If you like, tell us a little more about what "
            "you're looking for.")
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)



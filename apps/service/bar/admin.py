from django.contrib import admin
from apps.job.admin import JobRequestAdmin
from apps.freelancer.admin import FreelancerAdmin
from . import models


admin.site.register(models.BarFreelancer, FreelancerAdmin)
admin.site.register(models.BarJobRequest, JobRequestAdmin)

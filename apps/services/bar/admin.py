from django.contrib import admin
from apps.job.admin import JobRequestAdmin
from apps.freelancer.admin import FreelancerAdmin
from . import models


class BarFreelancerAdmin(admin.ModelAdmin):
    list_display = FreelancerAdmin.list_display + ('role',)

admin.site.register(models.BarFreelancer, BarFreelancerAdmin)


class BarJobRequestAdmin(JobRequestAdmin):
    list_display = JobRequestAdmin.list_display + ('role',)

admin.site.register(models.BarJobRequest, BarJobRequestAdmin)
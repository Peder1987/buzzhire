from django.contrib import admin
from apps.job.admin import JobRequestAdmin
from apps.freelancer.admin import FreelancerAdmin
from . import models


class ChefAdmin(admin.ModelAdmin):
    list_display = FreelancerAdmin.list_display + ('certification',)

admin.site.register(models.Chef, ChefAdmin)


class ChefJobRequestAdmin(JobRequestAdmin):
    list_display = JobRequestAdmin.list_display + ('certification',)

admin.site.register(models.ChefJobRequest, ChefJobRequestAdmin)

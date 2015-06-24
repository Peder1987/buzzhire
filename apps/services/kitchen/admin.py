from django.contrib import admin
from apps.job.admin import JobRequestAdmin
from apps.freelancer.admin import FreelancerAdmin
from . import models


class KitchenFreelancerAdmin(admin.ModelAdmin):
    list_display = FreelancerAdmin.list_display + ('certification',)

admin.site.register(models.KitchenFreelancer, KitchenFreelancerAdmin)


class KitchenJobRequestAdmin(JobRequestAdmin):
    list_display = JobRequestAdmin.list_display + ('certification',)

admin.site.register(models.KitchenJobRequest, KitchenJobRequestAdmin)

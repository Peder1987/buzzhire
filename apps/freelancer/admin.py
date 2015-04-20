from django.contrib import admin
from . import models

class FreelancerAdmin(admin.ModelAdmin):
    search_fields = ('first_name', 'last_name', 'user_email')

admin.site.register(models.Freelancer, FreelancerAdmin)

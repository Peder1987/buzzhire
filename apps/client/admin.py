from django.contrib import admin
from . import models


class LeadAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'created')


class ClientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'user',
                    'company_name', 'mobile')
    raw_id_fields = ('user',)
    search_fields = ('first_name', 'last_name',
                     'user__email')

admin.site.register(models.Lead, LeadAdmin)
admin.site.register(models.Client, ClientAdmin)

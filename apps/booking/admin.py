from django.contrib import admin
from . import models

class InvitationAdmin(admin.ModelAdmin):
    list_display = ('reference_number', 'freelancer', 'jobrequest',
                    'date_created', 'date_applied', 'date_declined', 'manual')
    search_fields = ('jobrequest', 'freelancer')
    raw_id_fields = ('jobrequest', 'freelancer')
    readonly_fields = ('date_created', 'date_applied', 'date_declined')
    list_filter = ('manual',)

admin.site.register(models.Invitation, InvitationAdmin)


class BookingAdmin(admin.ModelAdmin):
    list_display = ('reference_number', 'freelancer', 'jobrequest',
                    'date_created')
    search_fields = ('jobrequest', 'freelancer')
    raw_id_fields = ('jobrequest', 'freelancer')

admin.site.register(models.Booking, BookingAdmin)

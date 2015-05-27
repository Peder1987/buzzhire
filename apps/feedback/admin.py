from django.contrib import admin
from .models import BookingFeedback


class BookingFeedbackAdmin(admin.ModelAdmin):
    list_display = ('booking',
                    'author_type', 'score', 'comment')


admin.site.register(BookingFeedback, BookingFeedbackAdmin)

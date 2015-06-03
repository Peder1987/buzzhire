from django.contrib import admin
from .models import BookingFeedback


class BookingFeedbackAdmin(admin.ModelAdmin):
    def target(self, obj):
        target = obj.get_target()
        return '<a href="%s">%s</a>' % (target.get_absolute_url(),
                                        target)
    target.allow_tags = True

    def author(self, obj):
        author = obj.get_author()
        return '<a href="%s">%s</a>' % (author.get_absolute_url(),
                                        author)
    author.allow_tags = True

    list_display = ('booking', 'target', 'author',
                    'author_type', 'score', 'comment')


admin.site.register(BookingFeedback, BookingFeedbackAdmin)

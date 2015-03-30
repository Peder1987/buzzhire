from django.conf.urls import patterns, url
from apps.core.views import ContextTemplateView

urlpatterns = [
    url(r'^$', ContextTemplateView.as_view(
                    template_name='book/book.html',
                    extra_context={'title': 'Book a driver'}),
                    name='book'),

]

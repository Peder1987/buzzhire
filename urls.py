from django.conf.urls import include, url
from django.contrib import admin

def error(request):
    raise Exception

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', error)
]


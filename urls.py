from django.conf.urls import include, url, patterns
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^account/', include('apps.account.urls')),
    url(r'^freelancer/', include('apps.freelancer.urls')),
    url(r'^driver/', include('apps.driver.urls')),
    url(r'^client/', include('apps.client.urls')),
    url(r'^booking/', include('apps.booking.urls')),
    url(r'^job/', include('apps.job.urls')),
    url(r'^', include('apps.main.urls')),

]


if settings.DEBUG:
    urlpatterns += patterns('django.contrib.staticfiles.views',
        url(r'^static/(?P<path>.*)$', 'serve'),
    )
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

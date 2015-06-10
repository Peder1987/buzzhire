from django.conf.urls import patterns, url, include
from rest_framework import routers
from rest_framework.authtoken import views
from apps.booking.api.views import FreelancerBookingViewSet
from apps.freelancer.api.views import PublicFreelancerViewSet
from apps.client.api.views import PublicClientViewSet
from apps.job.api.views import JobRequestViewSet, DriverJobRequestViewSet
from apps.driver.api.views import VehicleTypeViewSet, FlexibleVehicleTypeViewSet
# This app is where we define the endpoints for the API,
# used by native mobile apps.

router = routers.DefaultRouter()
router.register(r'freelancers', PublicFreelancerViewSet,
                base_name='freelancers')
router.register(r'clients', PublicClientViewSet,
                base_name='clients')
router.register(r'vehicle-types/flexible', FlexibleVehicleTypeViewSet,
                base_name='flexible_vehicle_types')
router.register(r'vehicle-types', VehicleTypeViewSet,
                base_name='vehicle_types')

router.register(r'job-requests', JobRequestViewSet,
                base_name='job_requests')
router.register(r'driver-job-requests', DriverJobRequestViewSet,
                base_name='driver_job_requests')
router.register(r'bookings/for-freelancer', FreelancerBookingViewSet,
                base_name='bookings_for_freelancer')



urlpatterns = [
    url(r'^v1/auth/', include('rest_framework.urls',
                              namespace='rest_framework')),
    url(r'^v1/token-auth/', views.obtain_auth_token),
    url(r'^v1/', include(router.urls)),
]

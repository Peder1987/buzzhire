from django.conf.urls import patterns, url, include
from rest_framework.authtoken import views
from apps.booking.api.views import FreelancerBookingViewSet
from apps.freelancer.api.views import PublicFreelancerViewSet, \
                                    OwnFreelancerViewSet
from apps.client.api.views import PublicClientViewSet
from apps.job.api.views import JobRequestViewSet
from apps.service.driver.api.views import OwnDriverViewSet, \
        VehicleTypeViewSet, FlexibleVehicleTypeViewSet, DriverJobRequestViewSet
from apps.api.routers import SingleObjectFriendlyRouter

# This app is where we define the endpoints for the API,
# used by native mobile apps.


router = SingleObjectFriendlyRouter()
router.register(r'freelancers', PublicFreelancerViewSet,
                base_name='freelancers')
router.register(r'clients', PublicClientViewSet,
                 base_name='clients')
router.register(r'flexible-vehicle-types', FlexibleVehicleTypeViewSet,
                base_name='flexible_vehicle_types')
router.register(r'vehicle-types', VehicleTypeViewSet,
                base_name='vehicle_types')
router.register(r'job-requests', JobRequestViewSet,
                base_name='job_requests')
router.register(r'driver-job-requests', DriverJobRequestViewSet,
                base_name='driver_job_requests')
router.register(r'account/freelancer/bookings', FreelancerBookingViewSet,
                base_name='bookings_for_freelancer')
router.register(r'account/freelancer', OwnFreelancerViewSet,
                base_name='freelancer_own')
router.register(r'account/driver', OwnDriverViewSet,
                base_name='driver_own')


urlpatterns = [
    url(r'^v1/auth/', include('rest_framework.urls',
                              namespace='rest_framework')),
    url(r'^v1/token-auth/', views.obtain_auth_token),
    url(r'^v1/', include(router.urls)),

]

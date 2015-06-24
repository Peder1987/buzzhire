from django.conf.urls import patterns, url, include
from rest_framework.authtoken import views
from apps.booking.api.views import FreelancerBookingViewSet
from apps.freelancer.api.views import PublicFreelancerViewSet, \
                                    OwnFreelancerViewSet
from apps.client.api.views import PublicClientViewSet
from apps.job.api.views import JobRequestViewSet
from apps.api.routers import SingleObjectFriendlyRouter
from apps.services.driver.api.views import (OwnDriverViewSet,
    PublicDriverViewSet, VehicleTypeViewSet, FlexibleVehicleTypeViewSet,
    DriverJobRequestViewSet, DriverVehicleTypeViewSet)
from apps.services.cleaner.api.views import (PublicCleanerViewSet,
                                             OwnCleanerViewSet,
                                             CleanerJobRequestViewSet)
from apps.services.kitchen.api.views import (PublicKitchenFreelancerViewSet,
                                             OwnKitchenFreelancerViewSet,
                                             KitchenJobRequestViewSet)
from apps.services.bar.api.views import (PublicBarFreelancerViewSet,
                                             OwnBarFreelancerViewSet,
                                             BarJobRequestViewSet)
from apps.services.waiting.api.views import (PublicWaitingFreelancerViewSet,
                                             OwnWaitingFreelancerViewSet,
                                             WaitingJobRequestViewSet)

# This app is where we define the endpoints for the API,
# used by native mobile apps.

router = SingleObjectFriendlyRouter()

router.register(r'freelancers', PublicFreelancerViewSet,
                base_name='freelancers')
router.register(r'clients', PublicClientViewSet,
                 base_name='clients')
router.register(r'job-requests', JobRequestViewSet,
                base_name='job_requests')

router.register(r'account/freelancer/bookings', FreelancerBookingViewSet,
                base_name='bookings_for_freelancer')
router.register(r'account/freelancer', OwnFreelancerViewSet,
                base_name='freelancer_own')

# Driver specific
router.register(r'driver/freelancers', PublicDriverViewSet,
                base_name='driver_freelancers')
router.register(r'driver/account/freelancer', OwnDriverViewSet,
                base_name='driver_freelancer_own')
router.register(r'driver/account/vehicle-types', DriverVehicleTypeViewSet,
                base_name='driver_vehicle_types')

router.register(r'driver/job-requests', DriverJobRequestViewSet,
                base_name='driver_job_requests')
router.register(r'driver/vehicle-types', VehicleTypeViewSet,
                base_name='vehicle_types')
router.register(r'driver/flexible-vehicle-types', FlexibleVehicleTypeViewSet,
                base_name='flexible_vehicle_types')

# Cleaner specific
router.register(r'cleaner/freelancers', PublicCleanerViewSet,
                base_name='cleaner_freelancers')
router.register(r'cleaner/account/freelancer', OwnCleanerViewSet,
                base_name='cleaner_freelancer_own')
router.register(r'cleaner/job-requests', CleanerJobRequestViewSet,
                base_name='cleaner_job_requests')

# KitchenFreelancer specific
router.register(r'kitchen/freelancers', PublicKitchenFreelancerViewSet,
                base_name='kitchen_freelancers')
router.register(r'kitchen/account/freelancer', OwnKitchenFreelancerViewSet,
                base_name='kitchen_freelancer_own')
router.register(r'kitchen/job-requests', KitchenJobRequestViewSet,
                base_name='kitchen_job_requests')


# Bar specific
router.register(r'bar/freelancers', PublicBarFreelancerViewSet,
                base_name='bar_freelancers')
router.register(r'bar/account/freelancer', OwnBarFreelancerViewSet,
                base_name='bar_freelancer_own')
router.register(r'bar/job-requests', BarJobRequestViewSet,
                base_name='bar_job_requests')

# Waiting specific
router.register(r'waiting/freelancers', PublicWaitingFreelancerViewSet,
                base_name='waiting_freelancers')
router.register(r'waiting/account/freelancer', OwnWaitingFreelancerViewSet,
                base_name='waiting_freelancer_own')
router.register(r'waiting/job-requests', WaitingJobRequestViewSet,
                base_name='waiting_job_requests')


urlpatterns = [
    url(r'^v1/auth/', include('rest_framework.urls',
                              namespace='rest_framework')),
    url(r'^v1/token-auth/', views.obtain_auth_token),
    url(r'^v1/', include(router.urls)),

]

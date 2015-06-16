import calendar
from .models import Availability
from apps.job.models import JobRequest
from apps.freelancer.models import Freelancer, client_to_freelancer_rate
from apps.driver.models import Driver


class JobMatcher(object):
    """The workhorse for matching freelancers to job requests, or from a form.

    Usage:
        matcher = JobMatcher(job_request)
        freelancers = matcher.get_results()
    Or:
        matcher = JobMatcher(cleaned_data)
        freelancers = matcher.get_results()
    """

    def __init__(self, job_request_or_cleaned_data):
        if isinstance(job_request_or_cleaned_data, JobRequest):
            self.set_search_terms_from_job_request(job_request_or_cleaned_data)
        else:
            # Sets the search terms from the cleaned_data from a form
            self.search_terms = job_request_or_cleaned_data


    def set_search_terms_from_job_request(self, job_request):
        self.job_request = job_request
        self.search_terms = {}

        # Set initial for flat fields (i.e. ones that directly map between
        # form and job request attributes)
        FLAT_FIELDS = ('date', 'minimum_delivery_box', 'client_pay_per_hour',
                       'own_vehicle', 'phone_requirement')
        for field in FLAT_FIELDS:
            self.search_terms[field] = getattr(self.job_request, field)

        # Other fields
        self.search_terms['raw_postcode'] = str(self.job_request.postcode)
        self.search_terms['vehicle_type'] = self.job_request.vehicle_type

        self.search_terms['shift'] = Availability.shift_from_time(
                                                self.job_request.start_time)


    def get_results(self, ignore_availability=False):
        """Returns the freelancers that match the search terms.
        Optionally, can ignore the availability provided by the freelancers.
        """

        results = Driver.published_objects.all()

        results = self.filter_by_phone_requirement(results)
        results = self.filter_by_vehicle_requirements(results)
        if not ignore_availability:
            results = self.filter_by_availability(results)
        results = self.filter_by_pay_per_hour(results)
        results = self.filter_by_location(results)

        # Return unique results
        return results.distinct()

    def filter_by_phone_requirement(self, results):
        "Filters by the phone requirement."
        PHONE_REQUIREMENT_MAP = {
            JobRequest.PHONE_REQUIREMENT_NOT_REQUIRED: lambda r: r,
            JobRequest.PHONE_REQUIREMENT_ANY:
                lambda r: r.exclude(
                    phone_type__in=(Freelancer.PHONE_TYPE_NON_SMARTPHONE, '')),
            JobRequest.PHONE_REQUIREMENT_ANDROID:
                lambda r: r.filter(phone_type=Freelancer.PHONE_TYPE_ANDROID),
            JobRequest.PHONE_REQUIREMENT_IPHONE:
                lambda r: r.filter(phone_type=Freelancer.PHONE_TYPE_IPHONE),
            JobRequest.PHONE_REQUIREMENT_WINDOWS:
                lambda r: r.filter(phone_type=Freelancer.PHONE_TYPE_WINDOWS),
        }

        if self.search_terms['phone_requirement']:
            results = PHONE_REQUIREMENT_MAP[
                            self.search_terms['phone_requirement']](results)
        return results

    def filter_by_vehicle_requirements(self, results):
        "Filters by vehicle requirements."

        if self.search_terms['vehicle_type']:
            # The supplied vehicle type is a FlexibleVehicleType; unpack it
            # into individual VehicleTypes.
            vehicle_types = self.search_terms['vehicle_type'].as_queryset()
            if self.search_terms['own_vehicle']:
                # Filter by vehicle types that are owned
                filter_kwargs = {
                    'drivervehicletype__vehicle_type': \
                                    vehicle_types,
                    'drivervehicletype__own_vehicle': True
                }
                # Include delivery box filter, if specified
                if self.search_terms['minimum_delivery_box']:
                    filter_kwargs['drivervehicletype__delivery_box__gte'] = \
                                    self.search_terms['minimum_delivery_box']
                results = results.filter(**filter_kwargs)
            else:
                # Just filter by vehicle types
                filter_kwargs = {
                    'vehicle_types': vehicle_types
                }
            return results.filter(**filter_kwargs)

        return results

    def filter_by_availability(self, results):
        "Filters by availability, if it's been searched for."

        if self.search_terms['date']:

            # Get day of week for that date
            day_name = calendar.day_name[
                                self.search_terms['date'].weekday()].lower()

            # Build filter kwargs
            field_name = '%s_%s' % (day_name, self.search_terms['shift'])
            filter_kwargs = {'availability__%s' % field_name: True}

            # Filter
            results = results.filter(**filter_kwargs)

        return results

    def filter_by_pay_per_hour(self, results):
        """Filters the results based on the minimum pay per hour.
        This also sets self.freelancer_pay_per_hour in case client code
        needs to know it.
        """

        if self.search_terms['client_pay_per_hour']:
            self.freelancer_pay_per_hour = client_to_freelancer_rate(
                                    self.search_terms['client_pay_per_hour'])
            return results.filter(
                        minimum_pay_per_hour__lte=self.freelancer_pay_per_hour)
        return results

    def filter_by_location(self, results):
        """Filters the results by the supplied postcode, checking that it's
        within an acceptable distance for the driver."""
        if self.search_terms.get('postcode'):
            # Specific include distances so the template knows
            self.include_distances = True
            searched_point = self.search_terms['postcode'].point
            results = results.distance(searched_point,
                                       field_name='postcode__point')\
                        .order_by('distance')

            # if self.search_terms['respect_travel_distance']:
                # Filter by only those drivers whose travel distance works
                # with the postcode supplied
                # TODO - get this working with their personal distance settings
                # http://stackoverflow.com/questions/9547069/geodjango-distance-filter-with-distance-value-stored-within-model-query
                # results = results.filter(
                #      postcode__point__distance_lte=(searched_point, D(mi=4)))

        return results

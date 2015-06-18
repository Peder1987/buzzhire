from apps.booking.utils import JobMatcher


class DriverJobMatcher(JobMatcher):
    "JobMatcher tailored to matching drivers."

    flat_fields = JobMatcher.flat_fields + ('minimum_delivery_box',
                                            'own_vehicle')

    def set_search_terms_from_job_request(self, job_request):
        super(DriverJobMatcher, self).set_search_terms_from_job_request(
                                                                job_request)
        self.search_terms['vehicle_type'] = self.job_request.vehicle_type

    def get_results(self, *args, **kwargs):
        results = super(DriverJobMatcher, self).get_results(*args, **kwargs)
        results = self.filter_by_vehicle_requirements(results)
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
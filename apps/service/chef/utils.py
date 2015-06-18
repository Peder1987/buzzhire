from apps.booking.utils import JobMatcher


class ChefJobMatcher(JobMatcher):
    "JobMatcher tailored to matching chefs."

    flat_fields = JobMatcher.flat_fields + ('certification',)

    def get_results(self, *args, **kwargs):
        results = super(ChefJobMatcher, self).get_results(*args, **kwargs)
        results = self.filter_by_certification(results)
        return results

    def filter_by_certification(self, results):
        "Filters by certification."

        if self.search_terms['certification']:
            return results.filter(
                            certification=self.search_terms['certification'])

        return results

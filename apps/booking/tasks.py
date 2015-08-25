import time
from huey.djhuey import db_task
from .models import Invitation
from .signals import invitation_created
from apps.job import service_from_class


@db_task()
def invite_matching_freelancers(job_request):
    """Invites all suitable freelancers for the supplied job request. 
    """
    service = service_from_class(job_request.__class__)
    matcher = service.job_matching_form.job_matcher(job_request)
    freelancers = matcher.get_results(ignore_availability=True)
    for freelancer in freelancers:
        invitation, created = Invitation.objects.get_or_create(
                                               freelancer=freelancer,
                                               jobrequest=job_request)
        # Usually, the invitation won't exist - but just in case, we'll
        # only create invitations that haven't already been sent out
        if created:
            invitation_created.send(sender=invite_matching_freelancers,
                                invitation=invitation)
    print('[%s] Invited %d freelancers.' % (time.ctime(), freelancers.count()))

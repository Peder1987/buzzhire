from huey.djhuey import db_task
from apps.core.email import send_mail
from .models import Invitation
from .forms import JobMatchingForm
from .utils import JobMatcher
from .signals import invitation_created

@db_task()
def invite_matching_freelancers(job_request):
    """Invites all suitable freelancers for the supplied job request. 
    """
    matcher = JobMatcher(job_request)
    freelancers = matcher.get_results(ignore_availability=True)
    for freelancer in freelancers:
        invitation = Invitation.objects.create(freelancer=freelancer,
                                               jobrequest=job_request)
        invitation_created.send(sender=invite_matching_freelancers,
                                invitation=invitation)
    print('Invited %d freelancers.' % freelancers.count())

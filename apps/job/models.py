from django.db import models
from apps.core.utils import POUND_SIGN
from apps.provider.models import Specialism, Language, \
                                Skill, QualificationLevel
from django.core.urlresolvers import reverse
from private_media.storages import PrivateMediaStorage
from . import signals
from django.core.exceptions import ValidationError
from email.feedparser import NeedMoreData


class OpenJobRequestManager(models.Manager):
    "Job request manager for open job requests."
    def get_queryset(self):
        queryset = super(OpenJobRequestManager, self).get_queryset()
        return queryset.filter(status=JobRequest.STATUS_OPEN)


class JobRequest(models.Model):
    "A request by a client for a service."

    # The user who is making the job request
    client = models.ForeignKey('account.EmailUser',
                             related_name='job_requests')

    REGULARITY_TYPE_ONE_OFF = 'O'
    REGULARITY_TYPE_REGULAR = 'R'
    REGULARITY_TYPE_CHOICES = (
        (REGULARITY_TYPE_ONE_OFF, 'One off'),
        (REGULARITY_TYPE_REGULAR, 'Regular'),
    )

    regularity_type = models.CharField(
            'Is this a one off or a regular booking?',
            choices=REGULARITY_TYPE_CHOICES,
            default=REGULARITY_TYPE_ONE_OFF,
            max_length=1,
            help_text='Regular bookings involve appointments ' \
                    'that recur regularly.')

    location_address = models.TextField(
            help_text="Where the job will be.  " \
            "Please provide full address, including the postcode.")
    skill = models.ForeignKey(Skill, verbose_name='support needed')

    qualification_level = models.ForeignKey(QualificationLevel,
        verbose_name='level of qualification',
        blank=True, null=True)

    GENDER_ANY = 'A'
    GENDER_FEMALE = 'F'
    GENDER_MALE = 'M'
    GENDER_CHOICES = (
        (GENDER_ANY, 'Any'),
        (GENDER_FEMALE, 'Female'),
        (GENDER_MALE, 'Male'),
    )

    provider_gender = models.CharField('Gender needed', choices=GENDER_CHOICES,
                                       default=GENDER_ANY, max_length=2)

    language = models.ForeignKey(Language, blank=True, null=True)
    specialism = models.ForeignKey(Specialism,
                                   blank=True, null=True)
    number_of_providers = models.PositiveSmallIntegerField(
                                'Number of interpreters required',
                                choices=[(i, i) for i in range(1, 4)],
                                blank=True, null=True, default=1)
    job_date = models.DateField(blank=True, null=True)
    job_time = models.CharField('Time of the job', blank=True, max_length=25,
            help_text='Start time and end time.')

    INTERPRETING_METHOD_FACE_TO_FACE = 'FA'
    INTERPRETING_METHOD_VIDEO = 'VI'
    INTERPRETING_METHOD_CHOICES = (
        (INTERPRETING_METHOD_FACE_TO_FACE, 'Face to face'),
        (INTERPRETING_METHOD_VIDEO, 'Video'),
    )
    interpreting_method = models.CharField(max_length=2,
            default=INTERPRETING_METHOD_FACE_TO_FACE,
            choices=INTERPRETING_METHOD_CHOICES,
            help_text='For face to face, interpreters will travel to your '
                'location and interpret on site.  For video, you can use a '
                'laptop/computer to connect with an interpreter over video '
                '(suitable when you only require interpretation for a short '
                'amount of time).')

    budget = models.CharField('budget (inclusive of travel)',
            max_length=50,
            help_text="Budget in %s. Please specify whether or " \
                      "not the budget is for the whole job, " \
                      "or for the hourly rate." % POUND_SIGN)

    # This field is filled out by moderators
    provider_fee = models.CharField('LSP fee', max_length=50, blank=True,
                        help_text='The fee that will be paid to the LSP.')

    regular_booking_details = models.TextField('regular booking schedule',
                blank=True,
                help_text="""Please describe the dates and times of the
                regular booking.
                For example, 'Every Monday, 5pm - 6pm.'""")

    PAYMENT_ACCESS_TO_WORK = 'ATW'
    PAYMENT_CARD = 'CRD'
    PAYMENT_BACS = 'BAC'
    PAYMENT_SFE = 'SFE'
    PAYMENT_CHOICES = (
        (PAYMENT_ACCESS_TO_WORK, 'I am an Access to Work client'),
        (PAYMENT_CARD, 'Credit/debit card'),
        (PAYMENT_BACS, 'BACS'),
        (PAYMENT_SFE, 'I am a Student Finance England (SFE) client'),
    )
    payment_method = models.CharField(max_length=3, choices=PAYMENT_CHOICES)

    atw_letter = models.FileField('Access to Work letter',
              null=True, blank=True,
              upload_to='job/atw/%Y/%m/%d',
              help_text="Please attach evidence of your AtW budget.  If you "
                "have already provided your AtW proof then you don't  "
                "need to re-upload it.",
              storage=PrivateMediaStorage())
    overview = models.TextField('Job overview',
        help_text="""Please provide preparation for the language service
            provider (e.g. interpreter).  Preparation can include more specific
            details of the job, what the topic will be, or what the setting is.
            For example: 'I need support for an interview at a supermarket.  The
            interview will consist of questions on my past experiences
            and qualifications.'""")

    other_information = models.TextField(blank=True,
            help_text='Do you have any other information you want ' \
            'to give about the booking?')

    # Status - for admin purposes
    STATUS_NEW = 'NE'
    STATUS_OPEN = 'OP'
    STATUS_FOLLOW_UP = 'FU'
    STATUS_COMPLETE = 'CO'
    STATUS_CANCELLED = 'CA'
    STATUS_CHOICES = (
        (STATUS_NEW, 'New'),
        (STATUS_OPEN, 'Open'),
        (STATUS_FOLLOW_UP, 'Needs follow up'),
        (STATUS_COMPLETE, 'Complete'),
        (STATUS_CANCELLED, 'Cancelled'),
    )
    status = models.CharField(max_length=2, choices=STATUS_CHOICES,
                              default=STATUS_NEW)

    # The date this form was submitted
    date_submitted = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
    open_objects = OpenJobRequestManager()

    def __unicode__(self):
        return self.reference_number

    @property
    def reference_number(self):
        "Returns a reference number for this request."
        return 'JR%s' % str(self.pk).zfill(5)

    @property
    def full_name(self):
        return self.client.get_full_name()

    @property
    def email(self):
        return self.client.email

    @property
    def is_regular_booking(self):
        "Returns whether or not the job is a regular booking."
        return self.regularity_type == JobRequest.REGULARITY_TYPE_REGULAR

    def get_absolute_url(self):
        return reverse('jobrequest_detail', args=(self.pk,))

    def get_actions(self):
        "Returns actions that can be applied to this job request."
        actions = []
        if self.status != self.STATUS_OPEN and self.provider_fee:
            if self.status == self.STATUS_NEW:
                action_text = 'Open'
            else:
                action_text = 'Reopen'
            actions.append({'status': self.STATUS_OPEN,
             'action_text': action_text,
             'urlname': 'jobrequest_open'})

        if self.status == self.STATUS_OPEN:
            actions.append({'status': self.STATUS_COMPLETE,
             'action_text': 'Complete',
             'urlname': 'jobrequest_complete'})

        if self.status != self.STATUS_FOLLOW_UP:
            actions.append({'status': self.STATUS_FOLLOW_UP,
             'action_text': 'Needs follow up',
             'urlname': 'jobrequest_followup'})

        if self.status != self.STATUS_CANCELLED:
            actions.append({'status': self.STATUS_CANCELLED,
             'action_text': 'Cancel',
             'urlname': 'jobrequest_cancel'})

        return actions

    def update_status(self, status):
        """Updates the status to the supplied status, and saves.
        This should be used instead of simply changing the status,
        so the signal is trigger, and to support validation if we
        want to add this later. 
        """
        if self.status != status:
            original_status = self.status
            self.status = status
            self.save()

            # Dispatch signals
            if status == JobRequest.STATUS_OPEN:
                signals.jobrequest_opened.send(sender=JobRequest,
                                               jobrequest=self)
            elif status == JobRequest.STATUS_CANCELLED:
                signals.jobrequest_cancelled.send(sender=JobRequest,
                                                  jobrequest=self)
            elif status == JobRequest.STATUS_COMPLETE:
                signals.job_request_completed.send(sender=JobRequest,
                                                  job_request=self)

    class Meta:
        ordering = '-date_submitted',

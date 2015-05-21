from configurations_seddonym import StandardConfiguration
import os


class ProjectConfiguration(StandardConfiguration):
#     BASE_DIR = os.path.dirname(os.path.dirname(__file__))
#     STATICFILES_DIRS = (
#         os.path.join(BASE_DIR, "static"),
#     )
    SITE_TITLE = 'Buzzhire'
    PROJECT_NAME = 'buzzhire'
    INSTALLED_APPS = StandardConfiguration.INSTALLED_APPS + (
        # Apps lower down the list should import from apps higher up the list,
        # and not the other way around
        'django.contrib.humanize',
        'django.contrib.gis',
        'crispy_forms',
        'allauth',
        'allauth.account',
        'sorl.thumbnail',
        'django_extensions',
        'django_inlinecss',
        'compressor',
        'djangobower',
        'dbbackup',
        'fsm_admin',
        'django_bootstrap_breadcrumbs',
        'apps.core',
        'apps.location',
        'apps.account',
        'apps.freelancer',
        'apps.client',
        'apps.driver',
        'apps.payment',
        'apps.job',
        'apps.booking',
        'apps.feedback',
        'apps.main',
    )

    TEMPLATE_CONTEXT_PROCESSORS = StandardConfiguration.TEMPLATE_CONTEXT_PROCESSORS + (
         "allauth.account.context_processors.account",
         "allauth.socialaccount.context_processors.socialaccount",
         'apps.main.context_processors.main',
    )

    AUTHENTICATION_BACKENDS = (
        # Needed to login by username in Django admin, regardless of `allauth`
        "django.contrib.auth.backends.ModelBackend",

        # `allauth` specific authentication methods, such as login by e-mail
        "allauth.account.auth_backends.AuthenticationBackend",
    )

    CRISPY_TEMPLATE_PACK = 'bootstrap3'

    ACCOUNT_EMAIL_REQUIRED = True
    ACCOUNT_USERNAME_REQUIRED = False
    ACCOUNT_EMAIL_VERIFICATION = 'none'
    ACCOUNT_AUTHENTICATION_METHOD = 'email'
    ACCOUNT_USER_DISPLAY = 'apps.account.utils.user_display'

    FACEBOOK_URL = 'www.facebook.com/buzzhire.uk'
    TWITTER_URL = 'twitter.com/buzzhire'

    STATICFILES_FINDERS = StandardConfiguration.STATICFILES_FINDERS + (
        'compressor.finders.CompressorFinder',
        'djangobower.finders.BowerFinder',
    )

    COMPRESS_PRECOMPILERS = (
        ('text/less', 'lessc {infile} {outfile}'),
    )

    LOGIN_URL = 'account_login'
    CURRENCIES = ('GBP',)

    TIME_INPUT_FORMATS = ['%I:%M %p']

    def BOWER_COMPONENTS_ROOT(self):
        return os.path.join(self.PROJECT_ROOT, 'components')

    # The way django-bower is used in this project is that we run
    # ./manage.py bower install locally, to add the packages to
    # components/bower_components.  However, this is under version control
    # so bower install doesn't need to be run by the other installations.
    BOWER_INSTALLED_APPS = (
        'eternicode/bootstrap-datepicker',
        'acpmasquerade/bootstrap3-timepicker2',
        'bootstrap-star-rating',
    )

    @property
    def DEFAULT_DATABASE_ENGINE(self):
        # Location-based database
        return 'django.contrib.gis.db.backends.postgis'

    # Whether to show the holding site instead of the main site
    COMING_SOON = False

    # Min pay per hour, before commission
    CLIENT_MIN_WAGE = 8.0
    # The percent commission we charge on client rates
    COMMISSION_PERCENT = 15
    # Number of pence to round to
    COMMISSION_ROUND_PENCE = 25

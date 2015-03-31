from configurations_seddonym import StandardConfiguration
from configurations_seddonym.utils import classproperty
import os


class ProjectConfiguration(StandardConfiguration):
#     BASE_DIR = os.path.dirname(os.path.dirname(__file__))
#     STATICFILES_DIRS = (
#         os.path.join(BASE_DIR, "static"),
#     )
    PROTOCOL = 'http'
    SITE_TITLE = 'Buzzhire'
    PROJECT_NAME = 'buzzhire'
    INSTALLED_APPS = StandardConfiguration.INSTALLED_APPS + (
        # Apps lower down the list should import from apps higher up the list,
        # and not the other way around
        'django.contrib.humanize',
        'crispy_forms',
        'allauth',
        'allauth.account',
        'sorl.thumbnail',
        'django_extensions',
        'django_inlinecss',
        'compressor',
        'dbbackup',
        'django_bootstrap_breadcrumbs',
        'apps.core',
        'apps.account',
        'apps.freelancer',
        'apps.client',
        'apps.driver',
        'apps.booking',
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

    FACEBOOK_URL = 'www.facebook.com/buzzhire.uk'
    TWITTER_URL = 'twitter.com/buzzhire'

    STATICFILES_FINDERS = StandardConfiguration.STATICFILES_FINDERS + (
        'compressor.finders.CompressorFinder',
    )

    COMPRESS_PRECOMPILERS = (
        ('text/less', 'lessc {infile} {outfile}'),
    )

    LOGIN_URL = 'account_login'

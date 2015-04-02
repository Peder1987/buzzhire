from .project import ProjectConfiguration
from configurations_seddonym.utils import classproperty
import os
from django.conf.global_settings import DEFAULT_FROM_EMAIL


class Local(ProjectConfiguration):
    DEBUG = True
    DOMAIN = 'localhost'
    PORT = '8000'
    PROJECT_ROOT = '/home/david/www/buzzhire'
    MANAGERS = ADMINS = (
        ('David Seddon', 'david@seddonym.me'),
    )

    BOOKINGS_EMAIL = 'bookingslocal@dev.buzzhire.co'
    EMAIL_HOST_USER = 'buzzhire_dev'
    EMAIL_HOST = 'smtp.webfaction.com'

    @classmethod
    def get_default_from_email(cls):
        return 'local@dev.buzzhire.co'

    @classproperty
    def BASE_URL(cls):
        if getattr(cls, 'PORT', ''):
            # Necessary for the development server
            url = "%s:%s" % (cls.DOMAIN, cls.PORT)
        else:
            url = cls.DOMAIN
        return '%s://%s' % (cls.PROTOCOL, url)

    ACCOUNT_PASSWORD_MIN_LENGTH = 1

    @classmethod
    def get_static_root(cls):
        return ''

    @classproperty
    def STATICFILES_DIRS(cls):
        return (os.path.join(cls.get_setting('PROJECT_ROOT'), 'static'),)

    STATIC_ROOT = ''

    @classproperty
    def COMPRESS_ROOT(cls):
        return os.path.join(cls.get_setting('PROJECT_ROOT'), 'compressed')

    @classproperty
    def LOG_PATH(cls):
        return os.path.join('/var/log/django', cls.PROJECT_NAME)


class Dev(ProjectConfiguration):
    DEBUG = False
    DOMAIN = 'dev.buzzhire.co'
    WEBFACTION_USER = 'buzzhire'
    WEBFACTION_APPNAME = 'dev'

    EMAIL_HOST_USER = 'buzzhire_dev'
    EMAIL_HOST = 'smtp.webfaction.com'
    # TODO - get default from mail in form 'Buzzhire <contact@dev.buzzhire.co>'
    BOOKINGS_EMAIL = 'contact@buzzhire.co'

    MANAGERS = ADMINS = (
        ('David Seddon', 'david@seddonym.me'),
    )

    ACCOUNT_PASSWORD_MIN_LENGTH = 1

    @classproperty
    def PROJECT_ROOT(cls):
        return '/home/%s/webapps/%s/project' % (cls.WEBFACTION_USER, cls.WEBFACTION_APPNAME)

    @classproperty
    def BASE_URL(cls):
        return '%s://%s' % (cls.PROTOCOL, cls.DOMAIN)

    @classproperty
    def STATICFILES_DIRS(cls):
        return (os.path.join(cls.get_setting('PROJECT_ROOT'), 'static'),)

    @classproperty
    def LOG_PATH(cls):
        return '/home/%s/logs/user/%s/' % (cls.WEBFACTION_USER, cls.WEBFACTION_APPNAME)

    @classmethod
    def get_static_root(cls):
        return '/home/%s/webapps/%s/static' % (cls.WEBFACTION_USER, cls.WEBFACTION_APPNAME)

    @classmethod
    def get_media_root(cls):
        return '/home/%s/webapps/%s/uploads' % (cls.WEBFACTION_USER, cls.WEBFACTION_APPNAME)

    @classmethod
    def get_default_database_name(cls):
        return '%s_%s' % (cls.get_setting('PROJECT_NAME'),
                          cls.get_setting('WEBFACTION_APPNAME'))

    @classmethod
    def get_default_database_user(cls):
        return cls.get_default_database_name()


class Live(Dev):
    DEBUG = False
    DOMAIN = 'buzzhire.co'
    WEBFACTION_APPNAME = 'live'

    EMAIL_HOST_USER = 'buzzhire_live'
    EMAIL_HOST = 'smtp.webfaction.com'

    ACCOUNT_PASSWORD_MIN_LENGTH = 6

    AWS_ACCESS_KEY_ID = 'AKIAI7ZMKSCZQGQRGUJQ'
    AWS_BUCKET_NAME = 'buzzhire-backups-media'

    DBBACKUP_STORAGE = 'dbbackup.storage.s3_storage'
    DBBACKUP_S3_BUCKET = 'buzzhire-backups-db'

    @classproperty
    def DBBACKUP_S3_ACCESS_KEY(cls):
        return cls.AWS_ACCESS_KEY_ID

    @classproperty
    def DBBACKUP_S3_SECRET_KEY(cls):
        return cls.AWS_SECRET_ACCESS_KEY

    @classproperty
    def PROJECT_ROOT(cls):
        return '/home/%s/webapps/%s/project' % (cls.WEBFACTION_USER, cls.WEBFACTION_APPNAME)

    @classproperty
    def BASE_URL(cls):
        return '%s://%s' % (cls.PROTOCOL, cls.DOMAIN)

    @classproperty
    def STATICFILES_DIRS(cls):
        return (os.path.join(cls.get_setting('PROJECT_ROOT'), 'static'),)

    @classproperty
    def LOG_PATH(cls):
        return '/home/%s/logs/user/%s/' % (cls.WEBFACTION_USER, cls.WEBFACTION_APPNAME)


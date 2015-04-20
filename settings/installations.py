from .project import ProjectConfiguration
from configurations_seddonym import installations
import os


class Local(installations.LocalMixin, ProjectConfiguration):
    PROJECT_ROOT = '/home/david/www/buzzhire'
    BOOKINGS_EMAIL = 'bookingslocal@dev.buzzhire.co'
    EMAIL_HOST_USER = 'buzzhire_dev'
    EMAIL_HOST = 'smtp.webfaction.com'
    SERVER_EMAIL = 'local@dev.buzzhire.co'
    ACCOUNT_PASSWORD_MIN_LENGTH = 1


class Dev(installations.WebfactionDevMixin, ProjectConfiguration):
    DOMAIN = 'dev.buzzhire.co'
    WEBFACTION_USER = 'buzzhire'
    EMAIL_HOST_USER = 'buzzhire_dev'
    EMAIL_HOST = 'smtp.webfaction.com'
    ACCOUNT_PASSWORD_MIN_LENGTH = 1

    def BOOKINGS_EMAIL(self):
        return self.CONTACT_EMAIL


class Live(installations.WebfactionLiveMixin, ProjectConfiguration):
    DOMAIN = 'buzzhire.co'
    EMAIL_HOST_USER = 'buzzhire_live'
    ACCOUNT_PASSWORD_MIN_LENGTH = 6

    COMING_SOON = True

    AWS_ACCESS_KEY_ID = 'AKIAI7ZMKSCZQGQRGUJQ'
    AWS_BUCKET_NAME = 'buzzhire-backups-media'

    DBBACKUP_STORAGE = 'dbbackup.storage.s3_storage'
    DBBACKUP_S3_BUCKET = 'buzzhire-backups-db'

    @property
    def DBBACKUP_S3_ACCESS_KEY(self):
        return self.AWS_ACCESS_KEY_ID

    @property
    def DBBACKUP_S3_SECRET_KEY(self):
        return self.AWS_SECRET_ACCESS_KEY

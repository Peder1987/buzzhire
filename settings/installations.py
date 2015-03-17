from .project import ProjectConfiguration
from configurations_seddonym.utils import classproperty
import os


class Local(ProjectConfiguration):
    DEBUG = True
    DOMAIN = 'buzzhire.localhost'
    PROJECT_ROOT = '/home/david/www/buzzhire'
    MANAGERS = ADMINS = (
        ('David Seddon', 'david@seddonym.me'),
    )

    ACCOUNT_PASSWORD_MIN_LENGTH = 1

    @classproperty
    def MEDIA_ROOT(cls):
        return os.path.join(cls.get_setting('PROJECT_ROOT'), 'uploads')

    @classproperty
    def LOG_PATH(cls):
        return os.path.join('/var/log/django', cls.PROJECT_NAME)


class Dev(ProjectConfiguration):
    DEBUG = True

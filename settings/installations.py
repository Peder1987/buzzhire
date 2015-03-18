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

    @classproperty
    def BASE_URL(cls):
        return '%s://%s' % (cls.PROTOCOL, cls.DOMAIN)

    ACCOUNT_PASSWORD_MIN_LENGTH = 1

    @classmethod
    def get_static_root(cls):
        return ''

    @classproperty
    def STATICFILES_DIRS(cls):
        return (os.path.join(cls.get_setting('PROJECT_ROOT'), 'static'),)

    STATIC_ROOT = ''

    @classproperty
    def LOG_PATH(cls):
        return os.path.join('/var/log/django', cls.PROJECT_NAME)


class Dev(ProjectConfiguration):
    DEBUG = True

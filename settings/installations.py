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
    DOMAIN = 'dev.buzzhire.co'
    WEBFACTION_USER = 'buzzhire'
    WEBFACTION_APPNAME = 'dev'
    
    @classproperty
    def PROJECT_ROOT(cls):
        return '/home/%s/webapps/%s/project' % (cls.WEBFACTION_USER, cls.WEBFACTION_APPNAME)

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

    @classproperty
    def STATIC_ROOT(cls):
        return '/home/%s/webapps/%s_static/' % (cls.WEBFACTION_USER, cls.WEBFACTION_APPNAME)

    @classproperty
    def MEDIA_ROOT(cls):
        return '/home/%s/webapps/%s_uploads/' % (cls.WEBFACTION_USER, cls.WEBFACTION_APPNAME)

    @classproperty
    def LOG_PATH(cls):
        return '/home/%s/logs/user/%s/' % (cls.WEBFACTION_USER, cls.WEBFACTION_APPNAME)


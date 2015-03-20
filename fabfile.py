from fabric.api import *
from contextlib import contextmanager as _contextmanager
from fabric.contrib import files
from fabric import utils
import os
#==============================================================================
# Tasks which set up deployment environments
#==============================================================================

@task
def live():
    """
    Use the live deployment environment.
    """
    env.hosts = ['buzzhire.co']
    env.user = 'buzzhire'
    env.virtualenv_dir = '/home/buzzhire/.virtualenvs/live'
    env.code_dir = '/home/buzzhire/webapps/live/project'
    env.activate = 'source %s/bin/activate' % env.virtualenv_dir
    env.backup_on_deploy = False


@task
def dev():
    """
    Use the development deployment environment.
    """
    env.hosts = ['dev.buzzhire.co']
    env.user = 'buzzhire'
    env.virtualenv_dir = '/home/buzzhire/.virtualenvs/dev'
    env.code_dir = '/home/buzzhire/webapps/dev/project'
    env.activate = 'source %s/bin/activate' % env.virtualenv_dir
    env.backup_on_deploy = False

# Set the default environment.
dev()

@_contextmanager
def virtualenv():
    with cd(env.code_dir):
        with prefix(env.activate):
            yield

@task
def deploy(skip_backup=False):
    """
    To deploy and skip backup:
      fab deploy:'skip'
    """
    with virtualenv():
        run("git pull")
        run("pip install -r requirements.pip")

        if env.backup_on_deploy and not skip_backup:
            backup()

        run("touch wsgi.py")
        run("./manage.py migrate")
        run('./manage.py collectstatic --noinput')

@task
def backup():
    "Backs up the site uploaded files and database to Amazon S3."
    with virtualenv():
        run('./manage.py dbbackup')
        run('./manage.py mediabackup')

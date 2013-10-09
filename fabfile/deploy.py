import sys

from fabric.decorators import task
from fabric.api import cd, run
from fabric.context_managers import shell_env, settings
from fabric.contrib import django
from fabric.operations import sudo, os
from django.conf import settings as django_settings

from fabfile import get_environment, git_repo, virtualenv
from fabfile.db import migrate, create_db


def prepare_django_conf(environment):
    sys.path.append(environment.SITE_ROOT)
    os.environ['SuppressLogging'] = 'true'  # only key existense is checked
    os.environ['EnvironmentType'] = environment.NAME
    django.project('portal')


def activate_site(site_name="doc-approval"):
    sudo("a2ensite {0}".format(site_name))


def deactivate_site(site_name="doc-approval"):
    sudo("a2dissite {0}".format(site_name))


def restart_server():
    sudo("apache2ctl restart")


def install_packages():
    """Installs required OS packages"""
    sudo("apt-get -y install git")
    sudo("apt-get -y install apache2 libapache2-mod-wsgi")
    sudo("apt-get -y install postgresql postgresql-client postgresql-server-dev-9.1")
    sudo("apt-get -y install python-pip python2.7-dev")
    sudo("apt-get -y install libffi-dev libxml2-dev libxslt-dev")


def install_virtualenv():
    sudo("pip install virtualenv")
    sudo("pip install virtualenvwrapper")


def create_virtualenv(environment):
    with shell_env(WORKON_HOME='.virtualenvs'):
        run("source /usr/local/bin/virtualenvwrapper.sh && mkvirtualenv --no-site-packages %s" % environment.VENV)


def fetch_source_code(environment):
    with settings(warn_only=True):
        result = run("test -d {0}".format(environment.SITE_ROOT))
    if result.failed:
        run("mkdir {0}".format(environment.SITE_ROOT))
        run("git clone {0} -b {1} {2}".format(git_repo, environment.BRANCH, environment.SITE_ROOT))
    with cd(environment.SITE_ROOT):
        run("git pull")


def update_requirements(environment):
    with virtualenv(environment.VENV), cd(environment.SITE_ROOT + "/deployment"):
        run("pip install -r requirements.txt")


def create_log_and_upload_folders(environment):
    log_tpl = "mkdir -p {0} && chown -R {1}:{2} {0} && sudo chmod g+ws -R {0}"
    upload_tpl = "sudo mkdir -p {0} && sudo chown {1}:{2} {0} && sudo chmod 775 {0}"
    sudo(log_tpl.format(django_settings.LOGGING_DIRECTORY, environment.LOG_OWNER_USER, environment.LOG_OWNER_GROUP))
    sudo(upload_tpl.format(django_settings.MEDIA_ROOT, environment.LOG_OWNER_USER, environment.LOG_OWNER_GROUP))


def configure_apache(environment):
    with cd(environment.SITE_ROOT + "/deployment/apache-conf"):
        sudo("cp {0} /etc/apache2/sites-available/{1}".format(environment.APACHE_SITE_CONF, environment.SITE_NAME))
        deactivate_site(environment.SITE_NAME)
        activate_site(environment.SITE_NAME)
        deactivate_site("default")
        restart_server()


@task
def provision():
    """ Provisions initial installation"""
    environment = get_environment()
    # install_packages()
    install_virtualenv()
    create_virtualenv(environment)
    fetch_source_code(environment)
    update_requirements(environment)
    prepare_django_conf(environment)
    create_log_and_upload_folders(environment)
    create_db()
    configure_apache(environment)


@task
def deploy():
    environment = get_environment()
    # prepare_deploy()
    with cd(environment.SITE_ROOT):
        run("git pull")
    migrate()
    with cd(environment.SITE_ROOT):
        run("touch portal/wsgi.py")